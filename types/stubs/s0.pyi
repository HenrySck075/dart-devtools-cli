from typing import Literal, TypedDict


class FrameworkVersion(TypedDict):
    type: Literal["Success"]
    frameworkVersion: str
    channel: str
    repositoryUrl: str
    frameworkRevision: str
    frameworkCommitDate: str
    engineRevision: str
    dartSdkVersion: str
    devToolsVersion: str
    flutterVersion: str
    frameworkRevisionShort: str
    engineRevisionShort: str

    """
    type: "Success",
    frameworkVersion: "3.19.6",
    channel: "stable",
    repositoryUrl: "https://github.com/flutter/flutter.git",
    frameworkRevision: "54e66469a933b60ddf175f858f82eaeb97e48c8d",
    frameworkCommitDate: "2024-04-17 13:08:03 -0700",
    engineRevision: "c4cd48e186460b32d44585ce3c103271ab676355",
    dartSdkVersion: "3.3.4",
    devToolsVersion: "2.31.1",
    flutterVersion: "3.19.6",
    frameworkRevisionShort: "54e66469a9",
    engineRevisionShort: "c4cd48e186"
    """
