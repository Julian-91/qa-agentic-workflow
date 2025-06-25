from typing import TypedDict, Optional, List, Dict

class QaWorkflowState(TypedDict):
    url: str
    agents_needed: Optional[List[str]]
    reasoning: Optional[str]
    accessibility_scan_results: Optional[dict]
    security_test_results: Optional[dict]
    testcases_ui_test: Optional[List[dict]]
    testcases_accessibility_test: Optional[List[dict]]
    testcases_security_test: Optional[List[dict]]
    repo: str
    pr_number: int
    issue_number: Optional[int]
    github_issue: Optional[dict]
    pr_code_changes: Optional[str]
    ui_test_results: Optional[List[dict]]
    accessibility_scan_results: Optional[List[dict]]
    security_test_results: Optional[List[dict]]
    errors: Optional[List[str]]
    report: Optional[str]
