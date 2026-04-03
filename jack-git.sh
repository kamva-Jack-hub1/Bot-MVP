#!/bin/bash
# Jack's Git Manager - Team Sync Tool

cd ~/github/Bot-MVP

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}🦞 Jack's Git Manager${NC}"
echo "================================"
echo ""

# Check unpushed commits
UNPUSHED=$(git log origin/main..main --oneline 2>/dev/null | wc -l)
if [ "$UNPUSHED" -gt 0 ]; then
    echo -e "${YELLOW}⚠️ $UNPUSHED unpushed commits detected${NC}"
    git log origin/main..main --oneline
    echo ""
    echo -e "Push now? (y/n)"
    read -r push_now
    if [[ "$push_now" == "y" ]]; then
        git push origin main
        echo -e "${GREEN}✅ Pushed to GitHub${NC}"
    fi
else
    echo -e "${GREEN}✅ No unpushed commits${NC}"
fi

# Check status
echo ""
git status

# Check for uncommitted changes
if [[ -n $(git status -s) ]]; then
    echo ""
    echo -e "${YELLOW}📝 Uncommitted changes detected${NC}"
    echo "Add and commit? (y/n)"
    read -r add_commit
    
    if [[ "$add_commit" == "y" ]]; then
        git add .
        echo "Enter commit message:"
        read -r commit_msg
        git commit -m "$commit_msg"
        
        echo "Push now? (y/n)"
        read -r push_now2
        if [[ "$push_now2" == "y" ]]; then
            git push origin main
            echo -e "${GREEN}✅ Committed and pushed${NC}"
        else
            echo -e "${YELLOW}✅ Committed locally (not pushed)${NC}"
        fi
    fi
else
    echo -e "${GREEN}✅ No uncommitted changes${NC}"
fi

# Show recent activity
echo ""
echo -e "${BLUE}Recent commits:${NC}"
git log --oneline -5
