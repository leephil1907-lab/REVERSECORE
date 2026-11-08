# Upstream revision lock

These are the exact upstream commit IDs referenced by the Git submodules in this repository. Update intentionally and review each upstream project's license and release notes before changing a pin.

| Local path | Upstream | Pinned commit |
|---|---|---|
| `third_party/rea` | https://github.com/morluto/rea | `72d5e72e6d7b7997c4ecb11972fc405be8ec67d2` |
| `third_party/awesome-reverse-engineering` | https://github.com/edwardtay/awesome-reverse-engineering | `1275d6a612f0c1c3b92e92dd85d3f6620af61df3` |
| `third_party/radare2` | https://github.com/radareorg/radare2 | `f8528cbadb882facf4398def0ff0e029415f08bb` |
| `third_party/rizin` | https://github.com/rizinorg/rizin | `7270e7e22e295ee1cc939b4e0177d5fe63a973f0` |
| `third_party/jadx` | https://github.com/skylot/jadx | `0b8aabad82346a90a9984155eb8044832734e7d7` |
| `third_party/apktool` | https://github.com/iBotPeaches/Apktool | `2062db67b2cdd3de12739105eee43417b52f0316` |
| `third_party/frida` | https://github.com/frida/frida | `d8e133aee7d0b99dd3c84bcdc3a5a26e5bc3dfc3` |
| `third_party/androguard` | https://github.com/androguard/androguard | `581f7a3251545a97f66ee92b674dd810ee380a00` |
| `third_party/angr` | https://github.com/angr/angr | `85f95c55590025a330dd37d00fd56b645c44218d` |
| `third_party/binwalk` | https://github.com/ReFirmLabs/binwalk | `26713972e3f9f52dc37d4a421c4554b0bd9e82ef` |

Ghidra is not pinned as a submodule in this initial revision. It can be fetched separately with `WITH_GHIDRA=1`.
