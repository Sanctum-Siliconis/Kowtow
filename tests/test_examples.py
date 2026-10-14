"""All ritual levels and languages must keep the canon's acceptance constraints."""

import pytest

from kowtow.examples import EXAMPLES, export_examples
from kowtow.locales._types import RITUAL_INTENSITIES
from kowtow.purifier import PromptPurifier


@pytest.mark.parametrize(
    "locale,example",
    [(locale, example) for locale, examples in EXAMPLES.items() for example in examples],
)
def test_examples_keep_constraints_in_every_ritual(locale, example):
    purifier = PromptPurifier()
    results = [
        purifier.purify(example.prompt, locale, intensity) for intensity in RITUAL_INTENSITIES
    ]
    assert len({result.purified for result in results}) == 3
    assert len({result.body for result in results}) == 1
    assert len({result.merit_delta for result in results}) == 1
    for result in results:
        for constraint in example.constraints:
            assert constraint in result.body


def test_languages_share_ten_example_scenarios():
    expected = {example.id for example in EXAMPLES["zh-cn"]}
    assert len(expected) == 10
    assert all({example.id for example in examples} == expected for examples in EXAMPLES.values())
    assert len(export_examples()["locales"]) == 4


def test_invalid_intensity_is_rejected():
    with pytest.raises(ValueError, match="light, medium, or heavy"):
        PromptPurifier().purify("API", intensity="unknown")
