from pathlib import Path


REPO_ROOT = Path(__file__).parents[2]


def test_fceux_builder_writes_to_emu_dist_with_fceux_artifact_name():
    script = (REPO_ROOT / "build-fceux.ps1").read_text(encoding="utf-8")

    assert "dist\\emu" in script
    assert '".staging"' in script
    assert "z1rr-coop-$version-fceux-win32" in script
    assert "z1rr-coop-$version-fceux-win64" in script
    assert "dist\\fceux" not in script


def test_hardware_builder_writes_to_hardware_dist_with_hardware_artifact_name():
    script = (REPO_ROOT / "bridge" / "build-hardware.ps1").read_text(encoding="utf-8")

    assert "dist\\hardware" in script
    assert "z1rr-coop-$version-hardware.exe" in script
    assert "dist\\edn8" not in script


def test_build_all_uses_generic_distribution_targets():
    script = (REPO_ROOT / "build-all.ps1").read_text(encoding="utf-8")

    assert "dist/hardware/z1rr-coop-<version>-hardware.exe" in script
    assert "dist/emu/z1rr-coop-<version>-fceux-win32.zip" in script
    assert "dist/emu/z1rr-coop-<version>-fceux-win64.zip" in script
    assert 'label = "Hardware"' in script
    assert 'script = "bridge\\build-hardware.ps1"' in script
    assert "dist/edn8" not in script
    assert "dist/fceux" not in script


def test_legacy_edn8_builder_delegates_to_hardware_builder():
    script = (REPO_ROOT / "bridge" / "build-edn8.ps1").read_text(encoding="utf-8")

    assert "build-hardware.ps1" in script


def test_fceux_lua_modes_include_z1_and_chronogeran_modes():
    # Upstream z1rr-coop ships only the three Zelda 1 modes. This branch also
    # carries the additional game modes merged from chronogeran/emu-coop.
    mode_names = sorted(path.name for path in (REPO_ROOT / "modes").glob("*.lua"))

    for name in ["tloz_all.lua", "tloz_basic.lua", "tloz_progress.lua"]:
        assert name in mode_names

    index = (REPO_ROOT / "modes" / "index.lua").read_text(encoding="utf-8")
    for mode in ["modes.tloz_all", "modes.tloz_progress", "modes.tloz_basic"]:
        assert mode in index

    for name in ["lttp.lua", "lttp_randomizer.lua", "super_metroid.lua", "crystalis.lua"]:
        assert name in mode_names
        assert f'"modes.{name[:-4]}"' in index
