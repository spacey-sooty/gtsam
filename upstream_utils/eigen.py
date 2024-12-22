#!/usr/bin/env python3

"""
from wpilib. licensed under the wpilib license:

Copyright (c) 2009-2024 FIRST and other WPILib contributors
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
   * Redistributions of source code must retain the above copyright
     notice, this list of conditions and the following disclaimer.
   * Redistributions in binary form must reproduce the above copyright
     notice, this list of conditions and the following disclaimer in the
     documentation and/or other materials provided with the distribution.
   * Neither the name of FIRST, WPILib, nor the names of other WPILib
     contributors may be used to endorse or promote products derived from
     this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY FIRST AND OTHER WPILIB CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY NONINFRINGEMENT AND FITNESS FOR A PARTICULAR
PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL FIRST OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

import os
import re
import shutil

from upstream_utils import Lib, comment_out_invalid_includes, walk_cwd_and_copy_if


def eigen_inclusions(dp, f):
    """Returns true if the given file in the "Eigen" include directory of the
    Eigen git repo should be copied into allwpilib

    Keyword arguments:
    dp -- directory path
    f -- filename
    """
    if not dp.startswith(os.path.join(".", "Eigen")):
        return False

    abspath = os.path.join(dp, f)

    # Include architectures we care about
    if "Core/arch/" in abspath:
        return True

    return True


def unsupported_inclusions(dp, f):
    """Returns true if the given file in the "unsupported" include directory of
    the Eigen git repo should be copied into allwpilib

    Keyword arguments:
    dp -- directory path
    f -- filename
    """
    if not dp.startswith(os.path.join(".", "unsupported")):
        return False

    abspath = os.path.join(dp, f)

    # Exclude build system and READMEs
    if f == "CMakeLists.txt" or "README" in f:
        return False

    return True


def copy_upstream_src(wpilib_root):
    wpilib_root = os.path.join(wpilib_root, "")
    print(wpilib_root)

    # Delete old install
    for d in ["gtsam/3rdparty/Eigen"]:
        shutil.rmtree(os.path.join(wpilib_root, d), ignore_errors=True)

    # Upstream copies the whole enchilada, so let's do that too
    shutil.copytree(".", os.path.join(wpilib_root, "gtsam/3rdparty/Eigen"))

def main():
    name = "eigen"
    url = "https://gitlab.com/libeigen/eigen.git"
    # master on 2024-11-14
    tag = "0fb2ed140d4fc0108553ecfb25f2d7fc1a9319a1"

    eigen = Lib(name, url, tag, copy_upstream_src)
    eigen.main()


if __name__ == "__main__":
    main()
