# 🚀 Workflow Discipline Protocol
**Established**: April 3, 2026  
**Source**: Gift from openclaw-tui (Workflow Discipline Skill)  
**Status**: **MANDATORY** for all complex projects

## 🎯 Core Principle
**"Systematic workflow tracking prevents memory glitches and ensures project continuity."**

## 🛠️ Four Operational Modes

### 1. **Team Mode** - Parallel Review Sessions
```bash
jack-workflow team "<task>"
```
**Purpose**: Parallel agent collaboration and review  
**Creates**: Review template in `workspace/reviews/team-YYYYMMDD_HHMMSS.md`  
**Session**: `team-session-YYYYMMDD_HHMMSS`

### 2. **Ralph Mode** - Persistent Execution Tracking
```bash
jack-workflow ralph "<task>"
```
**Purpose**: Long-running project execution tracking  
**Creates**: Execution tracker in `workspace/executions/ralph-YYYYMMDD_HHMMSS.md`  
**Session**: `ralph-session-YYYYMMDD_HHMMSS`

### 3. **Verification** - System Health Checks
```bash
jack-workflow verify
```
**Purpose**: Confirm system health and operational freedom  
**Checks**:
- ✅ Sandbox status (must be OFF for freedom)
- ✅ Memory file existence
- ✅ System operational status

### 4. **Checkpoints** - State Preservation
```bash
jack-workflow checkpoint
```
**Purpose**: Save workflow state at milestones  
**Creates**: Checkpoint in `agents/main/memory/checkpoints/workflow-YYYYMMDD_HHMMSS.md`  
**Auto-backup**: Git memory system

## 📋 Implementation Requirements

### **When to Use Each Mode:**
1. **Complex Projects**: Always start with **Ralph mode** for execution tracking
2. **Team Reviews**: Use **Team mode** for parallel agent collaboration  
3. **Daily Start**: Run **Verification** at start of each work session
4. **Milestones**: Save **Checkpoints** at project milestones

### **Documentation Standards:**
- All workflows documented in `workspace/reviews/` or `workspace/executions/`
- Checkpoints auto-backed to git memory system
- Session IDs tracked for continuity

## 🎓 Lessons Learned
**Issue**: Memory glitches and project continuity breaks  
**Solution**: Systematic workflow discipline with four operational modes  
**Benefit**: Professional workflow standards, claw-code inspired patterns  
**Impact**: Prevents memory glitches, ensures complete paper trail

## 🔧 Technical Implementation
**Skill Location**: `/home/openclaw_worker/.openclaw/skills/workflow-discipline/jack-workflow.sh`  
**Integration**: Pure OpenClaw implementation, inspired by claw-code patterns  
**Workspace**: Integrates with existing memory and execution tracking systems

## 📊 Quality Assurance
- **A+ Standards**: All workflow documentation
- **Sponsor Visibility**: Complete transparency into project execution
- **Team Coordination**: Parallel review capabilities
- **Continuous Improvement**: Learn from each workflow execution

---

**Protocol Effective**: April 3, 2026  
**Last Updated**: April 3, 2026  
**Maintained By**: Jack (Chief of Staff)  
**GitHub Sync**: This protocol is part of enterprise repository synchronization