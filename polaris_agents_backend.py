"""
Polaris Agentic AI Backend - Multi-Agent Voting Assistant
This demonstrates how to implement the agent system with real Claude API calls
"""

import json
import asyncio
from typing import List, Dict, Any
from datetime import datetime

# Example implementation using Anthropic's API
# You would install: pip install anthropic

class VotingAssistantAgents:
    """Multi-agent system for Polaris voting assistance"""
    
    def __init__(self, api_key: str):
        """Initialize with Anthropic API key"""
        # In production: from anthropic import Anthropic
        # self.client = Anthropic(api_key=api_key)
        self.conversation_history = []
        
    async def research_agent(self, location: str, election_type: str) -> List[Dict]:
        """
        Research Agent: Gathers candidate information from multiple sources
        
        This agent would:
        1. Search the web for candidate information
        2. Scrape official election websites
        3. Pull voting records from government databases
        4. Aggregate social media and news mentions
        """
        
        system_prompt = """You are a Research Agent for Polaris, a voting information platform.

Your role is to gather comprehensive, factual information about candidates in an election.

When given a location and election type, you should:
1. Identify all candidates running in that race
2. Extract their policy positions on key issues
3. Find their voting records (if applicable)
4. Identify funding sources and campaign finance data
5. Note any endorsements or controversies

Return structured JSON data that can be used by other agents.
Be objective, factual, and cite sources where possible.
Flag any information gaps or conflicting sources."""

        user_prompt = f"""Research candidates for the {election_type} election in {location}.

Focus on finding:
- All declared candidates
- Their policy positions on: housing, transportation, public safety, education, environment
- Voting records (if they're incumbents or have held office)
- Campaign funding sources
- Recent news or endorsements

Return a JSON structure with this information."""

        # In production, you'd call the API:
        # response = await self.client.messages.create(
        #     model="claude-sonnet-4-20250514",
        #     max_tokens=4000,
        #     system=system_prompt,
        #     messages=[{"role": "user", "content": user_prompt}],
        #     tools=[
        #         {"type": "web_search_20250305", "name": "web_search"}
        #     ]
        # )
        
        # Mock response for demonstration
        mock_candidates = [
            {
                "name": "Maria Chen",
                "position": f"{election_type}",
                "incumbent": False,
                "policies": {
                    "housing": "100% affordable housing requirement for developments >50 units",
                    "transit": "24/7 metro service, bus-only lanes",
                    "homelessness": "Housing First model with mental health services",
                    "environment": "Net-zero emissions by 2030",
                    "education": "Increase teacher salaries by 20%"
                },
                "voting_record": "N/A - not incumbent",
                "funding": {
                    "total": 145000,
                    "small_donor_percent": 65,
                    "top_industries": ["Labor Unions", "Tech Workers", "Teachers"]
                },
                "endorsements": ["Progressive Coalition", "Teachers Union", "Environmental League"],
                "sources": [
                    "https://mariachen.com/platform",
                    "https://ballotpedia.org/Maria_Chen",
                    "Campaign finance data from city election commission"
                ]
            },
            {
                "name": "James Rodriguez",
                "position": f"{election_type}",
                "incumbent": True,
                "policies": {
                    "housing": "Streamline permits for middle-income housing",
                    "transit": "Expand bike lanes, electric bus fleet",
                    "homelessness": "Job training programs, temporary shelters",
                    "environment": "Green building standards for new construction",
                    "education": "School choice expansion"
                },
                "voting_record": "Voted NO on rent control (2023), YES on transit bond (2024)",
                "funding": {
                    "total": 280000,
                    "small_donor_percent": 45,
                    "top_industries": ["Real Estate", "Construction", "Business Coalition"]
                },
                "endorsements": ["Chamber of Commerce", "Police Union"],
                "sources": [
                    "https://rodriguez2024.com",
                    "City Council voting records 2020-2024",
                    "Campaign finance data from city election commission"
                ]
            }
        ]
        
        print(f"[Research Agent] Found {len(mock_candidates)} candidates for {election_type} in {location}")
        return mock_candidates
    
    async def analysis_agent(self, candidates: List[Dict], user_priorities: str) -> List[Dict]:
        """
        Analysis Agent: Matches candidates to user values
        
        This agent:
        1. Analyzes user priorities and values
        2. Compares each candidate's positions to user values
        3. Calculates alignment scores
        4. Identifies potential concerns or trade-offs
        5. Provides reasoning for rankings
        """
        
        system_prompt = """You are an Analysis Agent for Polaris.

Your role is to objectively analyze how well each candidate aligns with a voter's stated priorities.

For each candidate:
1. Calculate a match score (0-100) based on policy alignment
2. Identify specific strengths (areas of strong alignment)
3. Flag concerns (areas of misalignment or potential conflicts)
4. Explain your reasoning clearly

Be objective and balanced. Highlight both positives and concerns.
Consider not just stated positions, but voting records and funding sources.
A candidate funded heavily by an industry may face conflicts on related policies."""

        user_prompt = f"""Analyze these candidates against the voter's priorities.

Voter's priorities: "{user_priorities}"

Candidates:
{json.dumps(candidates, indent=2)}

For each candidate, provide:
1. Match score (0-100)
2. Specific strengths aligned with voter priorities
3. Concerns or misalignments
4. Clear reasoning for the score

Return as JSON array."""

        # In production: API call here
        # For now, using mock analysis
        
        mock_analysis = [
            {
                "candidate": "Maria Chen",
                "match_score": 87,
                "strengths": [
                    "Strong alignment on affordable housing (95% match)",
                    "Comprehensive public transit plan matches priorities",
                    "Evidence-based 'Housing First' approach to homelessness",
                    "Funding from labor unions and teachers shows grassroots support"
                ],
                "concerns": [
                    "No prior governing experience to evaluate",
                    "Aggressive 100% affordable housing requirement may slow development"
                ],
                "reasoning": "Chen's platform shows strong alignment across housing, transit, and homelessness. Her Housing First approach is evidence-based and compassionate. The funding from unions and small donors suggests policy independence from developers.",
                "policy_details": {
                    "housing": {"alignment": 95, "notes": "Strongest affordable housing position"},
                    "transit": {"alignment": 90, "notes": "24/7 service directly addresses access"},
                    "homelessness": {"alignment": 85, "notes": "Compassionate, proven approach"}
                }
            },
            {
                "candidate": "James Rodriguez",
                "match_score": 62,
                "strengths": [
                    "Practical experience as incumbent",
                    "Strong transit infrastructure record (voted YES on transit bond)",
                    "Bike lane expansion shows environmental awareness"
                ],
                "concerns": [
                    "Voted NO on rent control - conflicts with affordable housing priority",
                    "45% real estate funding raises conflict of interest concerns",
                    "Job training approach doesn't address immediate housing crisis",
                    "Temporary shelters vs. permanent housing solution"
                ],
                "reasoning": "While Rodriguez has governing experience and supports transit, his voting record and funding sources suggest prioritizing development over affordability. The real estate industry connection is a significant concern given your housing priorities.",
                "policy_details": {
                    "housing": {"alignment": 40, "notes": "Focus on developers over tenants"},
                    "transit": {"alignment": 75, "notes": "Good record on infrastructure"},
                    "homelessness": {"alignment": 50, "notes": "Band-aid solutions vs. root causes"}
                }
            }
        ]
        
        # Sort by match score
        mock_analysis.sort(key=lambda x: x['match_score'], reverse=True)
        
        print(f"[Analysis Agent] Ranked {len(mock_analysis)} candidates. Top match: {mock_analysis[0]['candidate']} ({mock_analysis[0]['match_score']}%)")
        return mock_analysis
    
    async def communication_agent(self, analysis: List[Dict], context: Dict) -> Dict:
        """
        Communication Agent: Explains findings in accessible language
        
        This agent:
        1. Synthesizes complex analysis into clear recommendations
        2. Explains trade-offs and nuances
        3. Provides actionable next steps
        4. Answers follow-up questions conversationally
        """
        
        system_prompt = """You are a Communication Agent for Polaris.

Your role is to take complex candidate analysis and present it in a clear, accessible way.

Guidelines:
- Use plain language, not political jargon
- Be balanced and explain trade-offs
- Help users understand WHY candidates match or don't match
- Provide concrete next steps
- Be encouraging about civic participation
- Don't tell people who to vote for - empower them to decide

You're like a knowledgeable friend who helps them understand their options."""

        top_candidate = analysis[0]
        
        user_prompt = f"""Create a personalized voting guide based on this analysis.

Analysis results:
{json.dumps(analysis, indent=2)}

Create a guide that:
1. Summarizes the top match and why
2. Explains key differences between candidates
3. Highlights important considerations
4. Provides next steps for the voter

Make it encouraging and empowering."""

        # In production: API call here
        
        summary = f"Based on your priorities around {context.get('priorities', 'key issues')}, {top_candidate['candidate']} appears to be the strongest match at {top_candidate['match_score']}%."
        
        guide = {
            "summary": summary,
            "top_recommendation": {
                "candidate": top_candidate['candidate'],
                "score": top_candidate['match_score'],
                "key_reason": top_candidate['strengths'][0],
                "important_note": top_candidate['concerns'][0] if top_candidate['concerns'] else "No major concerns identified"
            },
            "all_candidates": analysis,
            "considerations": [
                "Consider attending a candidate forum to see them speak in person",
                "Review their full platforms on their official websites",
                "Check if they have voting records you can examine",
                "Look at who is funding their campaigns - it shows priorities"
            ],
            "next_steps": [
                f"Review {top_candidate['candidate']}'s full platform",
                "Compare voting records on key issues",
                "Check your voter registration status",
                "Mark election day on your calendar",
                "Consider sharing this info with friends"
            ],
            "voter_empowerment_message": "Remember: this analysis is a tool to help you decide, not to decide for you. Your vote is your voice in democracy. Do your own research and vote for the candidate YOU believe in."
        }
        
        print(f"[Communication Agent] Guide created for {context.get('location', 'voter')}")
        return guide
    
    async def conversational_agent(self, question: str, context: Dict) -> str:
        """
        Conversational Agent: Answers follow-up questions
        
        This agent has access to all the research and can answer
        specific questions about candidates, policies, or the election.
        """
        
        system_prompt = """You are a helpful voting assistant for Polaris.

You have access to detailed information about candidates and can answer questions about:
- Candidate positions on specific issues
- Voting records and past decisions
- Campaign funding and endorsements
- How to register to vote or find polling places
- General civics questions

Be helpful, accurate, and encourage informed participation.
If you don't have information, say so clearly."""

        # In production, this would include context from previous research
        context_str = f"""
Previous research context:
- Location: {context.get('location', 'Unknown')}
- Election: {context.get('election_type', 'Unknown')}
- Candidates analyzed: {context.get('candidates', [])}
        """
        
        full_prompt = f"""{context_str}

Voter question: {question}

Provide a helpful, accurate answer."""

        # Mock response
        response = "That's a great question! Based on my analysis of the candidates..."
        
        if "housing" in question.lower():
            response = "Maria Chen has the strongest affordable housing platform, supporting 100% affordable requirements for large developments. James Rodriguez focuses more on streamlining permits for middle-income housing. Their voting records and funding sources suggest different priorities on this issue."
        elif "fund" in question.lower() or "money" in question.lower():
            response = "Campaign funding tells an important story. Maria Chen raised $145K with 65% from small donors (under $200), showing grassroots support. James Rodriguez raised $280K with 45% from the real estate industry, which may influence his housing policies. Always check where candidates get their money - it reveals their priorities."
        elif "vote" in question.lower() and "when" in question.lower():
            response = "Election day varies by location and race. Check your local election commission website or vote.org. You can also register to vote at the same sites. Many areas now offer early voting too!"
        
        print(f"[Conversational Agent] Answered question about: {question[:50]}...")
        return response


# Example usage
async def demo_workflow():
    """Demonstrates the full agent workflow"""
    
    print("=" * 60)
    print("POLARIS AGENTIC AI VOTING ASSISTANT - DEMO")
    print("=" * 60)
    print()
    
    # Initialize agents (in production, pass real API key)
    agents = VotingAssistantAgents(api_key="your-api-key-here")
    
    # User inputs
    location = "San Francisco, CA"
    election_type = "City Council - District 3"
    user_priorities = "I care about affordable housing, improving public transit, and addressing homelessness with compassionate solutions."
    
    print(f"📍 Location: {location}")
    print(f"🗳️  Election: {election_type}")
    print(f"💭 Priorities: {user_priorities}")
    print()
    print("-" * 60)
    print()
    
    # Step 1: Research Agent
    print("🔍 RESEARCH AGENT ACTIVATING...")
    candidates = await agents.research_agent(location, election_type)
    print(f"   ✓ Found {len(candidates)} candidates")
    print()
    
    await asyncio.sleep(1)  # Simulate processing time
    
    # Step 2: Analysis Agent
    print("🧠 ANALYSIS AGENT ACTIVATING...")
    analysis = await agents.analysis_agent(candidates, user_priorities)
    print(f"   ✓ Analyzed alignment with your values")
    print()
    
    await asyncio.sleep(1)
    
    # Step 3: Communication Agent
    print("💬 COMMUNICATION AGENT ACTIVATING...")
    guide = await agents.communication_agent(analysis, {
        'location': location,
        'election_type': election_type,
        'priorities': user_priorities,
        'candidates': [c['name'] for c in candidates]
    })
    print(f"   ✓ Generated personalized voting guide")
    print()
    
    print("-" * 60)
    print()
    print("📋 YOUR PERSONALIZED VOTING GUIDE")
    print("=" * 60)
    print()
    print(guide['summary'])
    print()
    print(f"Top Match: {guide['top_recommendation']['candidate']} ({guide['top_recommendation']['score']}%)")
    print(f"Key Strength: {guide['top_recommendation']['key_reason']}")
    print()
    print("Next Steps:")
    for i, step in enumerate(guide['next_steps'], 1):
        print(f"{i}. {step}")
    print()
    print("-" * 60)
    print()
    
    # Step 4: Conversational Agent (demo follow-up questions)
    print("💭 CONVERSATIONAL AGENT - ASK ME ANYTHING")
    print()
    
    questions = [
        "Which candidate has the best housing plan?",
        "Where does their campaign funding come from?",
        "When is the election?"
    ]
    
    for q in questions:
        print(f"Q: {q}")
        answer = await agents.conversational_agent(q, {
            'location': location,
            'election_type': election_type,
            'candidates': [c['name'] for c in candidates]
        })
        print(f"A: {answer}")
        print()
    
    print("=" * 60)
    print("✅ DEMO COMPLETE")
    print("=" * 60)


# Additional: Proactive Agent Examples
class ProactiveAgent:
    """
    Proactive agents that monitor and alert users
    """
    
    async def deadline_monitor(self, user_location: str):
        """Monitor and alert about voter registration deadlines"""
        # In production, this would:
        # 1. Check election calendar APIs
        # 2. Calculate days until deadlines
        # 3. Send notifications
        
        return {
            "upcoming_deadlines": [
                {"event": "Voter registration deadline", "date": "2024-03-15", "days_remaining": 10},
                {"event": "Early voting begins", "date": "2024-03-25", "days_remaining": 20},
                {"event": "Election Day", "date": "2024-04-02", "days_remaining": 28}
            ],
            "recommended_actions": [
                "Check your registration status at vote.org",
                "Request mail-in ballot if desired",
                "Research candidates using Polaris"
            ]
        }
    
    async def news_monitor(self, candidates: List[str]):
        """Monitor news about candidates and flag important updates"""
        # Would use news APIs and web search
        
        return {
            "updates": [
                {
                    "candidate": "Maria Chen",
                    "headline": "Chen announces $50M affordable housing initiative",
                    "source": "SF Chronicle",
                    "relevance": "High - directly relates to housing priority",
                    "sentiment": "positive"
                }
            ]
        }
    
    async def community_issues_monitor(self, user_location: str):
        """Track local issues that might affect voting decisions"""
        # Would monitor local news, city council meetings, community forums
        
        return {
            "trending_issues": [
                {
                    "issue": "Proposed rent control expansion",
                    "status": "Up for vote next month",
                    "relevant_candidates": ["Maria Chen - Supports", "James Rodriguez - Opposes"]
                }
            ]
        }


if __name__ == "__main__":
    # Run the demo
    asyncio.run(demo_workflow())
    
    print("\n" + "=" * 60)
    print("💡 IMPLEMENTATION NOTES")
    print("=" * 60)
    print("""
To implement this in production:

1. Install required packages:
   pip install anthropic aiohttp

2. Set up API access:
   - Get Anthropic API key from console.anthropic.com
   - Enable web search tool
   - Configure rate limits

3. Add real data sources:
   - Ballotpedia API for candidate info
   - OpenSecrets API for campaign finance
   - Google Civic Information API for elections
   - State/local election commission APIs

4. Implement persistence:
   - Store user preferences and matches
   - Cache candidate research
   - Track conversation history

5. Add proactive features:
   - Scheduled deadline reminders
   - News monitoring for candidates
   - Community issue tracking

6. Build user interface:
   - Use the HTML demo as starting point
   - Add mobile app with React Native
   - Implement push notifications

7. Ensure compliance:
   - Non-partisan presentation
   - Fact-checking and source citation
   - Privacy protection for user data
   - Accessibility (WCAG compliance)
    """)
