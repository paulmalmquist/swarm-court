"""Opt-in CLI skeleton: never invoked by the dashboard. NOT work-validated.
The default settings prevent all model calls. Admin/egress verification is an
external prerequisite, not something this module can infer from credentials.
"""
from __future__ import annotations
import argparse,json,os,shutil,subprocess
from pathlib import Path
from .ledger import Ledger

def gate(policy:dict,env:dict)->list[str]:
    issues=[]
    if not policy.get('execution_enabled'): issues.append('Execution is disabled')
    if not policy.get('admin_verified'): issues.append('Admin approval is unverified')
    if not policy.get('egress_approved'): issues.append('Context egress is unapproved')
    mode=policy.get('billing_mode')
    if mode not in ('included_allowance','consumption'): issues.append('Billing mode is unknown')
    if mode=='included_allowance' and not policy.get('usage_credits_disabled'): issues.append('Paid usage-credit control is unverified')
    if mode=='consumption' and (not policy.get('provider_spend_control_verified') or policy.get('metered_monthly_cap_usd',0)<=0):
        issues.append('Approved provider spend control and budget are required')
    if not policy.get('approved_model'): issues.append('No approved model configured')
    if policy.get('automatic_api_fallback'): issues.append('Automatic API fallback is forbidden')
    for name in ['ANTHROPIC_API_KEY','ANTHROPIC_AUTH_TOKEN','ANTHROPIC_BASE_URL','CLAUDE_CODE_USE_BEDROCK','CLAUDE_CODE_USE_VERTEX','CLAUDE_CODE_USE_FOUNDRY']:
        if env.get(name): issues.append(f'Provider override present: {name}; verify billing path explicitly')
    return issues

def run(packet:Path,root:Path)->dict:
    p=json.loads((root/'config/runtime.json').read_text()); reasons=gate(p,dict(os.environ))
    if reasons: raise RuntimeError('; '.join(reasons))
    binary=shutil.which('claude')
    if not binary: raise RuntimeError('Native Claude Code CLI not found')
    text=packet.read_text(encoding='utf-8')
    if len(text)>p['max_context_chars']: raise ValueError('Context packet exceeds configured character cap')
    cwd=root/'.runtime/isolated-run'; cwd.mkdir(parents=True,exist_ok=True)
    mcp=cwd/'empty-mcp.json'; mcp.write_text('{"mcpServers":{}}')
    command=[binary,'-p','Analyze the approved evidence packet on stdin. Return a bounded proposal with exact source references. Do not execute actions.',
        '--output-format','json','--model',p['approved_model'],'--effort','low',
        '--max-turns',str(p['max_turns_per_dispatch']),'--tools','',
        '--permission-mode','dontAsk','--strict-mcp-config','--mcp-config',str(mcp)]
    ledger=Ledger(root/'.runtime/court.sqlite3')
    rid=ledger.reserve_dispatch(p['max_dispatches_per_day'],p['max_wall_seconds'])
    try:
        result=subprocess.run(command,input=text,text=True,capture_output=True,cwd=cwd,timeout=p['max_wall_seconds'],check=False)
        if result.returncode: raise RuntimeError('Claude CLI failed; preserve task and inspect local CLI logs. No automatic retry.')
        payload=json.loads(result.stdout)
        if payload.get('is_error'): raise RuntimeError('Claude reported an error; task must be reviewed')
        ledger.finish_dispatch(rid,'proposal_received')
        return payload
    except BaseException:
        ledger.finish_dispatch(rid,'stopped_or_failed'); raise

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--packet',type=Path); parser.add_argument('--run',action='store_true')
    args=parser.parse_args(); root=Path(__file__).resolve().parents[1]
    if not args.run:
        print(json.dumps({'execution':'NOT STARTED','gates':gate(json.loads((root/'config/runtime.json').read_text()),dict(os.environ))},indent=2))
    elif not args.packet: parser.error('--packet is required for an explicit run')
    else: print(json.dumps(run(args.packet,root),indent=2))
