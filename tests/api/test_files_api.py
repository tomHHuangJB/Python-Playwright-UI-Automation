from __future__ import annotations

import pytest

from assertions.api_assertions import (
    assert_boolean,
    assert_integer,
    assert_non_empty_string,
    assert_required_keys,
    assert_response_header,
)


@pytest.mark.api
def test_upload_and_download_endpoints_expose_expected_headers_and_progress(
    api_client, data_factory
) -> None:
    upload_id = data_factory.unique_upload_id("api-upload")
    chunk_headers = {"upload-id": upload_id, "total-chunks": "3"}

    first_chunk = api_client.post_json(
        "/api/upload/chunk",
        headers={**chunk_headers, "chunk-index": "1"},
    )
    assert_required_keys(first_chunk, ("uploadId", "received", "total"))
    assert first_chunk["uploadId"] == upload_id
    assert_integer(first_chunk["received"], "received")
    assert_integer(first_chunk["total"], "total")
    assert first_chunk["received"] == 1
    assert first_chunk["total"] == 3

    incomplete_payload = api_client.post_json(
        "/api/upload/complete",
        headers={"upload-id": upload_id},
    )
    assert_required_keys(incomplete_payload, ("uploadId", "complete"))
    assert incomplete_payload["uploadId"] == upload_id
    assert_boolean(incomplete_payload["complete"], "complete")
    assert incomplete_payload["complete"] is False

    api_client.post_json("/api/upload/chunk", headers={**chunk_headers, "chunk-index": "2"})
    final_chunk = api_client.post_json(
        "/api/upload/chunk",
        headers={**chunk_headers, "chunk-index": "3"},
    )
    assert final_chunk["received"] == 3
    assert final_chunk["total"] == 3

    complete_payload = api_client.post_json(
        "/api/upload/complete",
        headers={"upload-id": upload_id},
    )
    assert complete_payload["complete"] is True

    download_response = api_client.get("/api/download/42")
    assert download_response.status_code == 200
    checksum = assert_response_header(download_response, "X-Checksum-Sha256")
    disposition = assert_response_header(download_response, "Content-Disposition")
    assert checksum == "demo-hash"
    assert "report-42.csv" in disposition
    assert_non_empty_string(download_response.text, "download body")
    assert "id,name" in download_response.text
