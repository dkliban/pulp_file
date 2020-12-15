#!/usr/bin/env bash
# coding=utf-8

set -mveuo pipefail


if [ "${GITHUB_REF##refs/tags/}" != "${GITHUB_REF}" ]
then
  PULPCORE_VERSION=$(http http://pulp/pulp/api/v3/status/ | jq -r '.versions'[0].version)
  cd ../pulpcore
  git checkout ${PULPCORE_VERSION} -- pulpcore/tests/
  cd ../pulp_file
fi

pytest -v -r sx --color=yes --pyargs pulp_file.tests.functional || show_logs_and_return_non_zero
pytest -v -r sx --color=yes --pyargs pulpcore.tests.functional || show_logs_and_return_non_zero
