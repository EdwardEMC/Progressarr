<script setup lang="ts">
import { computed, nextTick, onBeforeUnmount, onMounted, ref, useSlots, type VNode } from 'vue'

interface SelectOption {
  value: string
  label: string
  disabled: boolean
}

const props = withDefaults(
  defineProps<{
    modelValue: string
    id?: string
    ariaLabel?: string
    disabled?: boolean
  }>(),
  {
    id: undefined,
    ariaLabel: undefined,
    disabled: false,
  },
)

const emit = defineEmits<{
  'update:modelValue': [value: string]
}>()

const slots = useSlots()

const isOpen = ref(false)
const highlightedIndex = ref(-1)
const selectRef = ref<HTMLElement | null>(null)
const optionsRef = ref<HTMLElement | null>(null)

function getTextContent(node: VNode): string {
  if (typeof node.children === 'string') {
    return node.children.trim()
  }

  if (Array.isArray(node.children)) {
    return node.children
      .map((child) => {
        if (typeof child === 'string') {
          return child
        }

        if (typeof child === 'object' && child !== null) {
          return getTextContent(child as VNode)
        }

        return ''
      })
      .join('')
      .trim()
  }

  return ''
}

function extractOptions(nodes: VNode[]): SelectOption[] {
  const result: SelectOption[] = []

  for (const node of nodes) {
    /*
     * v-for can produce a Fragment VNode.
     * Recursively inspect its children so dynamically generated
     * <option> elements are found.
     */
    if (typeof node.type === 'symbol' && Array.isArray(node.children)) {
      result.push(
        ...extractOptions(
          node.children.filter(
            (child): child is VNode => typeof child === 'object' && child !== null,
          ),
        ),
      )

      continue
    }

    /*
     * Normal <option> VNodes.
     */
    if (node.type === 'option') {
      const nodeProps = node.props ?? {}

      result.push({
        value: String(nodeProps.value ?? ''),
        label: getTextContent(node),
        disabled: Boolean(nodeProps.disabled),
      })
    }
  }

  return result
}

const options = computed<SelectOption[]>(() => {
  const nodes = slots.default?.() ?? []
  return extractOptions(nodes)
})

const selectedOption = computed(() => {
  return options.value.find((option) => option.value === props.modelValue)
})

const selectedLabel = computed(() => {
  return selectedOption.value?.label ?? ''
})

const selectedIndex = computed(() => {
  return options.value.findIndex((option) => option.value === props.modelValue)
})

const enabledOptions = computed(() => {
  return options.value
    .map((option, index) => ({
      option,
      index,
    }))
    .filter(({ option }) => !option.disabled)
})

function open() {
  if (props.disabled || isOpen.value) {
    return
  }

  isOpen.value = true

  highlightedIndex.value =
    selectedIndex.value >= 0 ? selectedIndex.value : (enabledOptions.value[0]?.index ?? -1)

  nextTick(() => {
    scrollHighlightedOptionIntoView()
  })
}

function close() {
  isOpen.value = false
  highlightedIndex.value = -1
}

function toggle() {
  if (isOpen.value) {
    close()
  } else {
    open()
  }
}

function selectOption(index: number) {
  const option = options.value[index]

  if (!option || option.disabled) {
    return
  }

  emit('update:modelValue', option.value)
  close()
}

function moveHighlight(direction: 1 | -1) {
  if (!enabledOptions.value.length) {
    return
  }

  const currentPosition = enabledOptions.value.findIndex(
    ({ index }) => index === highlightedIndex.value,
  )

  let nextPosition = currentPosition + direction

  if (currentPosition === -1) {
    nextPosition = direction === 1 ? 0 : enabledOptions.value.length - 1
  }

  if (nextPosition < 0) {
    nextPosition = enabledOptions.value.length - 1
  }

  if (nextPosition >= enabledOptions.value.length) {
    nextPosition = 0
  }

  highlightedIndex.value = enabledOptions.value[nextPosition]?.index ?? -1

  nextTick(() => {
    scrollHighlightedOptionIntoView()
  })
}

function selectHighlighted() {
  if (highlightedIndex.value >= 0) {
    selectOption(highlightedIndex.value)
  }
}

function handleKeydown(event: KeyboardEvent) {
  if (props.disabled) {
    return
  }

  switch (event.key) {
    case 'Enter':
    case ' ':
      event.preventDefault()

      if (isOpen.value) {
        selectHighlighted()
      } else {
        open()
      }

      break

    case 'ArrowDown':
      event.preventDefault()

      if (!isOpen.value) {
        open()
      } else {
        moveHighlight(1)
      }

      break

    case 'ArrowUp':
      event.preventDefault()

      if (!isOpen.value) {
        open()
      } else {
        moveHighlight(-1)
      }

      break

    case 'Escape':
      if (isOpen.value) {
        event.preventDefault()
        close()
      }

      break

    case 'Home':
      if (isOpen.value) {
        event.preventDefault()

        const first = enabledOptions.value[0]

        if (first) {
          highlightedIndex.value = first.index

          nextTick(() => {
            scrollHighlightedOptionIntoView()
          })
        }
      }

      break

    case 'End':
      if (isOpen.value) {
        event.preventDefault()

        const last = enabledOptions.value[enabledOptions.value.length - 1]

        if (last) {
          highlightedIndex.value = last.index

          nextTick(() => {
            scrollHighlightedOptionIntoView()
          })
        }
      }

      break
  }
}

function handleClickOutside(event: MouseEvent) {
  if (selectRef.value && !selectRef.value.contains(event.target as Node)) {
    close()
  }
}

function scrollHighlightedOptionIntoView() {
  if (!optionsRef.value || highlightedIndex.value < 0) {
    return
  }

  const element = optionsRef.value.querySelector(`[data-option-index="${highlightedIndex.value}"]`)

  if (element instanceof HTMLElement) {
    element.scrollIntoView({
      block: 'nearest',
    })
  }
}

onMounted(() => {
  document.addEventListener('mousedown', handleClickOutside)
})

onBeforeUnmount(() => {
  document.removeEventListener('mousedown', handleClickOutside)
})
</script>

<template>
  <div ref="selectRef" class="relative w-full">
    <!--
      Keep the slot in the component API so callers can continue
      using normal <option> elements.
      The slot itself is hidden because this component does not
      use the browser's native <select> UI.
    -->
    <div class="hidden">
      <slot />
    </div>

    <button
      :id="id"
      type="button"
      role="combobox"
      :aria-label="ariaLabel"
      :aria-expanded="isOpen"
      aria-haspopup="listbox"
      :disabled="disabled"
      class="flex w-full items-center justify-between rounded-lg border bg-white px-3 py-2.5 text-left text-sm outline-none transition disabled:cursor-not-allowed disabled:opacity-50 dark:bg-zinc-950"
      :class="
        isOpen
          ? 'border-zinc-400 ring-1 ring-zinc-400 dark:border-zinc-500 dark:ring-zinc-500'
          : 'border-zinc-300 hover:border-zinc-400 dark:border-zinc-700 dark:hover:border-zinc-600'
      "
      @click="toggle"
      @keydown="handleKeydown"
    >
      <span
        class="min-w-0 flex-1 truncate"
        :class="selectedOption ? 'text-zinc-900 dark:text-white' : 'text-zinc-500'"
      >
        {{ selectedLabel }}
      </span>

      <svg
        class="ml-3 h-4 w-4 shrink-0 text-zinc-500 transition-transform duration-150"
        :class="{ 'rotate-180': isOpen }"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        stroke-width="2"
      >
        <path d="m6 9 6 6 6-6" />
      </svg>
    </button>

    <div
      v-if="isOpen"
      ref="optionsRef"
      role="listbox"
      :aria-labelledby="id"
      class="absolute left-0 right-0 z-50 mt-2 max-h-60 overflow-y-auto rounded-lg border border-zinc-200 bg-white p-1 shadow-2xl dark:border-zinc-700 dark:bg-zinc-900"
    >
      <button
        v-for="(option, index) in options"
        :key="`${option.value}-${index}`"
        type="button"
        role="option"
        :aria-selected="option.value === modelValue"
        :disabled="option.disabled"
        :data-option-index="index"
        class="flex w-full items-center rounded-md px-3 py-2.5 text-left text-sm transition"
        :class="
          option.disabled
            ? 'cursor-not-allowed text-zinc-400 dark:text-zinc-600'
            : index === highlightedIndex
              ? 'bg-zinc-100 text-zinc-900 dark:bg-zinc-800 dark:text-white'
              : 'text-zinc-700 hover:bg-zinc-100 hover:text-zinc-900 dark:text-zinc-300 dark:hover:bg-zinc-800 dark:hover:text-white'
        "
        @mouseenter="highlightedIndex = index"
        @click="selectOption(index)"
      >
        <span class="min-w-0 flex-1 truncate">
          {{ option.label }}
        </span>

        <svg
          v-if="option.value === modelValue"
          class="ml-3 h-4 w-4 shrink-0 text-purple-600 dark:text-purple-400"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="2.5"
        >
          <path d="m5 12 4 4L19 6" />
        </svg>
      </button>
    </div>
  </div>
</template>
