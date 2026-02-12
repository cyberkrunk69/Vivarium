-- CI Status GUI — One-click wrapper for ci-status dry-run + execute
-- Run dry-run, show cost in dialog, on Yes open Terminal and run execute.
-- Place this app in devtools/; it locates scripts relative to itself.

on run
	-- Resolve paths: app is at REPO_ROOT/devtools/ci-status-gui.app
	-- container of app = devtools; container of that = repo root
	set repoRoot to POSIX path of (container of (container of (path to me)))
	if repoRoot ends with "/" then
		set repoRoot to text 1 thru -2 of repoRoot
	end if
	set dryRunScript to repoRoot & "/devtools/_internal/ci-status/ci-status-dry-run.sh"
	set executeScript to repoRoot & "/devtools/_internal/ci-status/ci-status-execute.sh"
	
	-- Run dry-run and capture output
	set dryRunOutput to ""
	try
		set repoRootQ to quoted form of repoRoot
		set dryRunScriptQ to quoted form of dryRunScript
		set dryRunOutput to do shell script "cd " & repoRootQ & " && " & dryRunScriptQ & " 2>&1"
	on error errMsg number errNum
		display dialog "CI Status Dry Run Failed" & return & return & errMsg buttons {"OK"} default button 1 with icon stop with title "CI Status"
		return
	end try
	
	-- Parse cost line: "Estimated Groq API cost: $X.XX for N job(s)."
	-- Or: "No AI summarization needed (no failed jobs or GROQ_API_KEY not set)."
	set costMessage to ""
	set hasCostLine to false
	repeat with line in paragraphs of dryRunOutput
		set line to line as text
		if line contains "Estimated Groq API cost:" then
			set costMessage to line
			set hasCostLine to true
			exit repeat
		else if line contains "No AI summarization needed" then
			set costMessage to "No API costs (no failed jobs or GROQ_API_KEY not set)."
			set hasCostLine to true
			exit repeat
		end if
	end repeat
	
	if not hasCostLine then
		-- Check for failure indicators
		if dryRunOutput contains "❌" then
			display dialog "CI Status Dry Run Failed" & return & return & "Could not parse output. Check for errors:" & return & return & (last paragraph of dryRunOutput) buttons {"OK"} default button 1 with icon stop with title "CI Status"
		else
			display dialog "CI Status Dry Run" & return & return & "Could not parse estimated cost from output." & return & return & "Dry run may have completed. You can run the execute script manually from Terminal." buttons {"OK"} default button 1 with icon caution with title "CI Status"
		end if
		return
	end if
	
	-- Show confirmation dialog
	set dialogMessage to costMessage & return & return & "Execute with this cost?"
	set reply to display dialog dialogMessage buttons {"No", "Yes"} default button 2 cancel button 1 with icon 1 with title "CI Status"
	
	if button returned of reply is "Yes" then
		-- Open Terminal and run execute (pipe "y" to auto-confirm)
		tell application "Terminal"
			activate
			do script "cd " & quoted form of repoRoot & " && VIVARIUM_CONFIRM_AI=1 " & quoted form of executeScript
		end tell
	end if
end run
