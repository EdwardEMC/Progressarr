from app.services.download_service import DownloadService
from app.models import DownloadStatus


def test_calculate_progress():
    progress = DownloadService._calculate_progress(
        size=1000,
        size_remaining=250,
    )

    assert progress == 75.0


def test_calculate_progress_zero_size():
    progress = DownloadService._calculate_progress(
        size=0,
        size_remaining=0,
    )

    assert progress == 0.0


def test_calculate_progress_never_exceeds_100():
    progress = DownloadService._calculate_progress(
        size=1000,
        size_remaining=-100,
    )

    assert progress == 100.0


def test_calculate_progress_never_below_zero():
    progress = DownloadService._calculate_progress(
        size=1000,
        size_remaining=1500,
    )

    assert progress == 0.0


def test_status_downloading():
    status = DownloadService._get_status({
        "status": "downloading",
    })

    assert status == DownloadStatus.DOWNLOADING


def test_status_queued():
    status = DownloadService._get_status({
        "status": "queued",
    })

    assert status == DownloadStatus.DOWNLOADING


def test_status_import_pending():
    status = DownloadService._get_status({
        "status": "completed",
        "trackedDownloadState": "importPending",
    })

    assert status == DownloadStatus.IMPORT_PENDING


def test_status_import_blocked():
    status = DownloadService._get_status({
        "status": "completed",
        "trackedDownloadState": "importBlocked",
    })

    assert status == DownloadStatus.FAILED


def test_status_completed():
    status = DownloadService._get_status({
        "status": "completed",
    })

    assert status == DownloadStatus.COMPLETED


def test_status_unknown():
    status = DownloadService._get_status({
        "status": "somethingUnexpected",
    })

    assert status == DownloadStatus.UNKNOWN
    