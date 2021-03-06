from insights.core import dr

stage = dr.new_component_type(type_metadata={"description": "A processing stage."})


@stage()
def report(broker):
    return "this is a regular report"


@stage(metadata={"description": "Reports stuff about things."})
def special_report(broker):
    return "this is a special report"


def test_component_metadata():
    msg = "A processing stage."
    special_msg = "Reports stuff about things."
    assert dr.get_metadata(report).get("description") == msg
    assert dr.get_metadata(special_report).get("description") == special_msg
