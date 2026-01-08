# Project Learnings & Issues

## Environment Setup
**Issue:** Python packages installed in different environments (Anaconda vs system Python)  
**Impact:** `ModuleNotFoundError` for pandas / matplotlib  
**Fix:** Standardized on a single Python environment and installed packages using `pip install` from the active terminal  
**Takeaway:** Always verify which Python interpreter is executing the script

---

## File Path Errors
**Issue:** `FileNotFoundError` when loading CSV  
**Cause:** Script executed from a different working directory  
**Fix:** Used absolute paths via `Path(__file__).parent`  
**Takeaway:** Relative paths depend on execution context

---

## Column Name Inconsistencies
**Issue:** `KeyError: 'activity'` during grouping  
**Cause:** Extra whitespace and inconsistent casing in column names  
**Fix:** Normalized column names using `str.strip().str.lower()`  
**Takeaway:** Always standardize schema before analysis

---

## Visualization Behavior
**Issue:** Pie chart did not display in certain environments  
**Fix:** Saved chart to file (`.png`) as a reliable output  
**Takeaway:** Persist visual outputs rather than relying on interactive display
