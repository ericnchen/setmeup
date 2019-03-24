# -*- coding: utf-8 -*-
from click.testing import CliRunner
from pytest import fixture

from setmeup.cli import main


@fixture
def runner():
    return CliRunner()


def test_install_yes_can_be_enabled(runner):
    assert runner.invoke(main, ["install", "--yes"]).exit_code == 0


def test_install_backup_can_be_disabled(runner):
    assert runner.invoke(main, ["install", "--nobackup"]).exit_code == 0


def test_install_all_can_be_enabled(runner):
    assert runner.invoke(main, ["install", "--all"]).exit_code == 0


def test_install_missing_can_be_enabled(runner):
    assert runner.invoke(main, ["install", "--missing"]).exit_code == 0


def test_install_all_and_missing_cannot_be_both_enabled(runner):
    assert runner.invoke(main, ["install", "--all", "--missing"]).exit_code != 0


def test_install_one_filename_can_be_given(runner):
    assert runner.invoke(main, ["install", ".bashrc"]).exit_code == 0


def test_install_two_filenames_can_be_given(runner):
    assert runner.invoke(main, ["install", ".bashrc", ".bash_profile"]).exit_code == 0


def test_install_filename_and_all_cannot_both_be_enabled(runner):
    assert runner.invoke(main, ["install", "--all", ".bashrc"]).exit_code != 0


def test_install_filename_and_missing_cannot_both_be_enabled(runner):
    assert runner.invoke(main, ["install", "--missing", ".bashrc"]).exit_code != 0


def test_list_all_can_be_enabled(runner):
    assert runner.invoke(main, ["list", "--all"]).exit_code == 0


def test_list_missing_can_be_enabled(runner):
    assert runner.invoke(main, ["list", "--missing"]).exit_code == 0


def test_list_installed_can_be_enabled(runner):
    assert runner.invoke(main, ["list", "--installed"]).exit_code == 0


def test_list_all_and_missing_cannot_be_both_enabled(runner):
    assert runner.invoke(main, ["list", "--all", "--missing"]).exit_code != 0


def test_list_all_and_installed_cannot_be_both_enabled(runner):
    assert runner.invoke(main, ["list", "--all", "--missing"]).exit_code != 0


def test_list_installed_and_missing_cannot_be_both_enabled(runner):
    assert runner.invoke(main, ["list", "--installed", "--missing"]).exit_code != 0


def test_list_all_installed_and_missing_cannot_be_all_enabled(runner):
    assert runner.invoke(main, ["list", "-aim"]).exit_code != 0


def test_list_all_installed_and_missing_cannot_be_all_disabled(runner):
    assert runner.invoke(main, ["list"]).exit_code != 0


def test_list_full_can_be_enabled_for_installed(runner):
    assert runner.invoke(main, ["list", "--installed", "--full"]).exit_code == 0


def test_list_full_cannot_be_enabled_for_all(runner):
    assert runner.invoke(main, ["list", "--all", "--full"]).exit_code != 0


def test_list_full_cannot_be_enabled_for_missing(runner):
    assert runner.invoke(main, ["list", "--missing", "--full"]).exit_code != 0


def test_update_yes_can_be_enabled(runner):
    assert False


def test_update_yes_defaults_to_false(runner):
    assert False


def test_update_all_can_be_enabled(runner):
    assert False


def test_update_missing_can_be_enabled(runner):
    assert False


def test_update_installed_can_be_enabled(runner):
    assert False


def test_update_all_and_missing_cannot_be_both_enabled(runner):
    assert False


def test_update_all_and_installed_cannot_be_both_enabled(runner):
    assert False


def test_update_installed_and_missing_cannot_be_both_enabled(runner):
    assert False


def test_update_all_and_installed_and_missing_cannot_be_all_enabled(runner):
    assert False


def test_update_one_filename_can_be_given(runner):
    assert False


def test_update_two_filenames_can_be_given(runner):
    assert False


def test_update_filename_cannot_be_given_with_all(runner):
    assert False


def test_update_filename_cannot_be_given_with_installed(runner):
    assert False


def test_update_filename_cannot_be_given_with_missing(runner):
    assert False


def test_uninstall_yes_can_be_enabled(runner):
    assert False


def test_uninstall_yes_defaults_to_false(runner):
    assert False


def test_uninstall_restore_can_be_enabled(runner):
    assert False


def test_uninstall_restore_defaults_to_true(runner):
    assert False


def test_uninstall_all_can_be_given(runner):
    assert False


def test_uninstall_one_filename_can_be_given(runner):
    assert False


def test_uninstall_two_filenames_can_be_given(runner):
    assert False


def test_uninstall_all_and_filename_cannot_be_given(runner):
    assert False
