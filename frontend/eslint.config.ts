import eslint from '@eslint/js'
import tseslint from 'typescript-eslint'
import vue from 'eslint-plugin-vue'

export default [
  {
    ignores: ['dist', 'node_modules'],
  },

  eslint.configs.recommended,

  ...vue.configs['flat/recommended'],

  ...tseslint.configs.recommended,

  {
    files: ['**/*.{ts,vue}'],
    rules: {
      'no-console': 'warn',
    },
  },
]