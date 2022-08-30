import pprint
import os
import re
import svn.local
import svn.remote
import pysvn

from .repo_wrapper import RepoWrapper

class LogEntry:
    def __init__(self, log_header, log_msg):
        self.log_header = log_header
        self.log_msg = log_msg
        self.feature_number = None
        self.user = None
        self.release = None

        if rslt_release := re.search("r([0-9]*)", log_header, re.IGNORECASE):
            self.release = rslt_release.group(1)
        if rslt_feature := re.search("F#([0-9]*)", log_msg, re.IGNORECASE):
            self.feature_number = rslt_feature.group(1)
        if rslt_user := re.search(r"\| ([a-zA-Z]*) \|", log_header, re.IGNORECASE):
            self.user = rslt_user.group(1)

    def process_diff(self, diff_str):
        result = []

        diff_strs = diff_str.split("Index:")
        for dstr in diff_strs:
            if dstr:
                file_name = ""
                changed_lines = []
                for dlines in dstr.split("\n"):
                    if rslt_file_name := re.search(r"\-\-\- ([a-zA-Z.]*)", dlines):
                        file_name = rslt_file_name.group(1)
                    if rslt_file_name := re.search(r"\+\+\+ ([a-zA-Z.]*)", dlines):
                        file_name = rslt_file_name.group(1)
                    if rslt_line_change := re.search(r"\+ ([a-zA-Z.\*\+\-\*\/:\(\) ]*)", dlines):
                        changed_lines.append(rslt_line_change.group(1))
                    if rslt_line_change := re.search(r"\- ([a-zA-Z.\*\+\-\*\/:\(\) ]*)", dlines):
                        changed_lines.append(rslt_line_change.group(1))
                result.append(DiffEntry(file_name, changed_lines))

        self.diffs = result


class DiffEntry:
    def __init__(self, changed_file, changed_lines):
        self.changed_file = changed_file
        self.changed_lines = changed_lines


class SVNWrapper(RepoWrapper):
    """
    Wrapper to manipulate SVN repository

    """

    def process_log_result(self, log_list):
        result = []

        for log_entry in log_list:
            log_entry = log_entry.split("\n\n")
            header = log_entry[0]
            message = ""
            diff = ""

            if len(log_entry) >= 2:
                message = log_entry[1]
                if len(log_entry) >= 3:
                    diff = log_entry[2]

                log_entry_obj = LogEntry(log_entry[0], log_entry[1])
                log_entry_obj.process_diff(log_entry[2])
                result.append(log_entry_obj)

        return result

    async def udpate_repo(self):
        self.repo = pysvn.Client("/var/git/" + self.repo_path)
        # self.repo.get_login("http://svn-compatible/svn/project_2", username="admin", password="admin")
        # await print(self.repo.log(decoding = 'utf8'))
        # await log("/var/git/" + self.repo_path, os.environ.get("SVN_USER"), os.environ.get("SVN_PASSWORD"))
        last_commit = None
        logs = self.process_log_result(await log("http://svn-compatible/svn/project_2", os.environ.get("SVN_USER"), os.environ.get("SVN_PASSWORD")))
        logs.reverse()
        for i in logs:
            print("NOVA ENTRADA LOG")
            print(f"HEADER {i.log_header}")
            print(f"RELEASE {i.release}")
            print(f"FEATURE {i.feature_number}")
            print(f"USER {i.user}")
            print(f"MSG {i.log_msg}")
            for j in i.diffs:
                print(f"ARQUIVO MODIFICADO {j.changed_file}")
                for l in j.changed_lines:
                    print(f"LINHA MODIFICADA {l}")
            print(("FINAL"))
            print()
            print()

            last_commit = i.release

        return last_commit
        # self.repo = svn.local.LocalClient("/var/git/" + self.repo_path,
        #                                   username=os.environ.get("SVN_USER"),
        #                                   password=os.environ.get("SVN_PASSWORD"))

        # # self.repo = svn.remote.RemoteClient("http://svn-compatible/svn/project_2",
        # #                                   username=os.environ.get("SVN_USER"),
        # #                                   password=os.environ.get("SVN_PASSWORD"))

        # print("Antes de buscar", dir(self.repo))
        # print(self.repo.log_default(rel_filepath="log.xml", revision_from='1'))
        # # pprint.pprint(self.repo.log_default())
        # for t in self.repo.log_default(rel_filepath="log.xml", revision_from='1'):
        #     print(t)

        # for i in self.repo.diff_summary(old=1, new=2):
        #     print(i)
        # # self.repo.update()

        # # client = pysvn.Client("/var/git/" + self.repo_path)
        # # print(client.log())
        # # for e in self.repo.log_default():
        # #     print(e)

#!/usr/bin/env python
import os
import subprocess
import sys
import asyncio

async def call_cmd(cmd):
    proc = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)

    stdout, stderr = await proc.communicate()
    return stdout.decode()

async def log(repo, username, password):
    cmd = ' '.join(["svn", "log", repo, "--username", username, "--password", password, "--diff"])
    result = await call_cmd(cmd)
    print("SVN", result)
    return result.split('-' * 72)


# svn log http://svn-compatible/svn/project_2 --username admin --password admin