# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os, sys

from command import Command
from sync import Sync

class Clone(Command):
  common = True
  helpSummary = "Performs the initial clone for all repos and checks out master"
  helpUsage = """
%prog
"""
  def Execute(self, opt, args):
    if os.path.exists(os.path.join(self.repodir, "projects")):
      print >>sys.stderr, "this working directory has already been cloned into. exiting."
      sys.exit(1)

    #run Sync to clone the repos into the tree the way Repo expects them
    sync_cmd = Sync()
    sync_cmd.NAME = 'sync'
    sync_cmd.manifest = self.manifest
    sync_cmd.repodir = self.repodir
    argv = sys.argv
    argv = argv[argv.index('--')+2:]
    newopts, newargs = sync_cmd.OptionParser.parse_args(argv)
    sync_cmd.Execute(newopts, newargs)

    #checkout master everywhere
    for project in self.GetProjects(''):
      print >>sys.stdout, "%s:" % project.name
      out = project.work_git.checkout("-t", "-b", "master", "remotes/origin/master")
      print >>sys.stdout, out
      print >>sys.stdout
