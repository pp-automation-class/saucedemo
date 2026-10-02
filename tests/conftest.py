"""Steps shared by more than one feature + pytest-bdd hooks."""

import logging

from tests.cucumber import given, when

log = logging.getLogger("bdd")


# ---------- pytest-bdd hooks ----------
# Each hook writes one line to logs/test_run.log, prefixed with its own name.
# Step args are not logged: they can hold a password.


def pytest_bdd_apply_tag(tag, function):
    log.info("[pytest_bdd_apply_tag] @%s -> %s", tag, function.__name__)
    # None = let pytest-bdd apply the tag as a marker (default behaviour).
    return None


def pytest_bdd_before_scenario(request, feature, scenario):
    log.info("[pytest_bdd_before_scenario] %s: %s", feature.name, scenario.name)


def pytest_bdd_after_scenario(request, feature, scenario):
    log.info("[pytest_bdd_after_scenario] %s: %s", feature.name, scenario.name)


def pytest_bdd_before_step(request, feature, scenario, step, step_func):
    log.info("[pytest_bdd_before_step] %s %s", step.keyword, step.name)


def pytest_bdd_before_step_call(
    request, feature, scenario, step, step_func, step_func_args
):
    log.info("[pytest_bdd_before_step_call] %s()", step_func.__name__)


def pytest_bdd_after_step(request, feature, scenario, step, step_func, step_func_args):
    log.info("[pytest_bdd_after_step] %s %s", step.keyword, step.name)


def pytest_bdd_step_error(
    request, feature, scenario, step, step_func, step_func_args, exception
):
    log.error(
        "[pytest_bdd_step_error] %s %s -> %s: %s",
        step.keyword,
        step.name,
        type(exception).__name__,
        exception,
    )


def pytest_bdd_step_func_lookup_error(request, feature, scenario, step, exception):
    log.error(
        "[pytest_bdd_step_func_lookup_error] no step definition for: %s %s",
        step.keyword,
        step.name,
    )


# ---------- shared steps ----------


@given("a standard user is logged in")
def standard_user_is_logged_in(logged_in):
    return logged_in


@when("the user adds {string} to the cart")
def user_adds_product(logged_in, string):
    logged_in.add_to_cart(string)
