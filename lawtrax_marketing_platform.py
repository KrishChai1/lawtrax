"""
LawTrax Marketing Command Center
A comprehensive marketing platform for SEO, content generation, and lead generation
Built for immigration software marketing teams
"""

import streamlit as st
import anthropic
from datetime import datetime
import json
import re

# Page Configuration
st.set_page_config(
    page_title="Marketing Command Center",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
st.markdown("""
<style>
    /* Main theme colors */
    :root {
        --primary-color: #4B0082;
        --secondary-color: #7B68EE;
        --accent-color: #9370DB;
        --success-color: #32CD32;
        --warning-color: #FFA500;
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(135deg, #4B0082 0%, #7B68EE 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
    }
    
    .main-header h1 {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    .main-header p {
        font-size: 1.1rem;
        opacity: 0.9;
    }
    
    /* Card styling */
    .metric-card {
        background: linear-gradient(145deg, #ffffff 0%, #f5f5f5 100%);
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        border-left: 4px solid #4B0082;
        margin-bottom: 1rem;
    }
    
    .feature-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
        border: 1px solid #e0e0e0;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }
    
    /* Platform badges */
    .platform-badge {
        display: inline-block;
        padding: 0.4rem 1rem;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.85rem;
        margin: 0.25rem;
    }
    
    .linkedin-badge { background: #0077B5; color: white; }
    .instagram-badge { background: linear-gradient(45deg, #f09433, #e6683c, #dc2743, #cc2366, #bc1888); color: white; }
    .tiktok-badge { background: #000000; color: white; }
    .youtube-badge { background: #FF0000; color: white; }
    .twitter-badge { background: #1DA1F2; color: white; }
    .facebook-badge { background: #4267B2; color: white; }
    
    /* Content output styling */
    .content-output {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid #dee2e6;
        margin-top: 1rem;
    }
    
    /* Success message */
    .success-banner {
        background: linear-gradient(135deg, #32CD32 0%, #228B22 100%);
        color: white;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
        margin: 1rem 0;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #f0f2f6;
        border-radius: 8px 8px 0 0;
        padding: 10px 20px;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #4B0082;
        color: white;
    }
    
    /* Sidebar styling */
    .sidebar-header {
        text-align: center;
        padding: 1rem;
        background: linear-gradient(135deg, #4B0082 0%, #7B68EE 100%);
        border-radius: 10px;
        color: white;
        margin-bottom: 1rem;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #4B0082 0%, #7B68EE 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: scale(1.02);
        box-shadow: 0 5px 20px rgba(75, 0, 130, 0.4);
    }
    
    /* Info boxes */
    .info-box {
        background: #e3f2fd;
        border-left: 4px solid #2196F3;
        padding: 1rem;
        border-radius: 0 8px 8px 0;
        margin: 1rem 0;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'generated_content' not in st.session_state:
    st.session_state.generated_content = []
if 'company_profile' not in st.session_state:
    st.session_state.company_profile = {}
if 'api_key' not in st.session_state:
    # Try to get API key from Streamlit secrets first
    try:
        st.session_state.api_key = st.secrets.get("CLAUDE_API_KEY", "") or st.secrets.get("ANTHROPIC_API_KEY", "")
    except Exception:
        st.session_state.api_key = ""

# Company Knowledge Base (Default: LawTrax)
LAWTRAX_KNOWLEDGE = """
COMPANY: LawTrax
TAGLINE: "Immigration Software for the Modern Attorney"
WEBSITE: lawtrax.com

CORE VALUE PROPOSITION:
LawTrax is a secure, cloud-based immigration case management platform that empowers attorney firms to manage leads, clients, and cases effortlessly. The platform enables customizable workflows, seamless carrier label generation, and integrated invoice management.

KEY FEATURES:
1. Case Management - Workflow-based platform with multiple stages based on case type, enabling end-to-end management, tracking, and stakeholder notifications
2. Customer Management - Secure cloud portal for companies/beneficiaries to manage information and initiate cases with single-click automation
3. Lead Management - Built-in CRM for converting prospects to customers with lead categorization and tracking
4. Document Management - Cloud-based, indexable, searchable system with three stages: identification, generation, and delivery
5. Dashboard Reporting - Real-time business-driven dashboards with drill-down capabilities and configurable KPIs
6. PDF Generation - Auto-generates USCIS/DoL formatted documents based on case type rules
7. Client Portal - Secure document uploads and case status tracking with automated notifications
8. Integration Capabilities - Outlook calendar, QuickBooks billing, webhooks, and RESTful APIs

SECURITY & COMPLIANCE:
- Multi-tenant architecture on Google Cloud Platform with Firebase
- SOC 2 Type II certification (in pipeline)
- GDPR compliance (in pipeline)
- HIPAA compliant architecture
- End-to-end encryption for data at rest and in transit
- Role-based access control with SSO support
- California Consumer Privacy Act (CCPA) compliance
- PCI compliance with digital tokens for authentication

TECHNICAL SPECIFICATIONS:
- Cloud-hosted on Google Cloud Platform
- Multi-tenant SaaS with broker patterns for tenant isolation
- RESTful APIs with no additional costs
- Real-time reporting (no batch delays)
- 99.9% uptime guarantee on Google infrastructure
- Automatic OCR capabilities
- Real-time form updates from USCIS

KEY DIFFERENTIATORS:
1. No additional API costs (unlike competitors)
2. True real-time reporting without 24-hour batch delays
3. Guaranteed uptime on Google's enterprise infrastructure
4. Built-in PDF generator for USCIS/DoL formatted submissions
5. Comprehensive audit trail for all document actions
6. Customizable email templates and notification engine

CLIENT SUCCESS METRICS:
- Clients report 30%+ revenue increase
- Reduced administrative burden
- Faster case completion through digital automation
- Increased capacity for new clients

TARGET MARKET:
- Immigration law firms (solo to enterprise)
- Corporate immigration departments
- Global mobility teams
- Legal service providers

CONTACT:
- Email: info@lawtrax.com
- Phone: 972-200-1030
- Address: 17400 Dallas Parkway, Suite 121, Dallas, Texas 75287
"""

# Platform-specific content guidelines
PLATFORM_GUIDELINES = {
    "LinkedIn": {
        "max_chars": 3000,
        "hashtags": 5,
        "tone": "Professional, thought leadership focused, storytelling",
        "format": "Long-form posts, carousel documents, polls, articles",
        "best_practices": [
            "Start with a HOOK - first line must stop the scroll (use pattern interrupts, bold claims, or curiosity gaps)",
            "One sentence per line - creates white space and readability",
            "Use line breaks after EVERY sentence for mobile readability",
            "Keep paragraphs to 1-2 lines maximum",
            "Include a 'pattern interrupt' halfway through (→, •, ↓, or emoji)",
            "Tell a story or share a personal insight - LinkedIn rewards authenticity",
            "End with a question or call-to-engagement to boost comments",
            "Add 3-5 relevant hashtags at the VERY END (not mixed in)",
            "Use 'I' statements and first-person narrative",
            "Best posting times: Tue-Thu, 8-10am or 12-1pm user's timezone",
            "Optimal length: 1,200-1,500 characters for maximum engagement",
            "NO external links in post body (kills reach) - put in comments",
            "Use emojis sparingly (1-3 max) for visual breaks"
        ],
        "content_types": ["Thought leadership", "Industry insights", "Case studies", "Company updates", "Employee spotlights", "How-to guides", "Hot takes", "Lessons learned", "Behind-the-scenes"],
        "viral_hooks": [
            "I spent [X years/hours] doing [thing]. Here's what I learned:",
            "Stop doing [common practice]. Do this instead:",
            "[Controversial opinion]. Here's why:",
            "Most [persona] get this wrong about [topic].",
            "The biggest mistake I see [persona] make:",
            "[Number] [things] that will [benefit] in [timeframe]:",
            "Unpopular opinion: [statement]",
            "I was wrong about [thing]. Here's the truth:",
            "This changed everything for our [clients/business]:",
            "[Persona], you need to hear this:"
        ]
    },
    "Instagram": {
        "max_chars": 2200,
        "hashtags": 20,
        "tone": "Visual, engaging, authentic",
        "format": "Carousel posts, Reels, Stories, Feed posts",
        "best_practices": [
            "Lead with value in the first line",
            "Use emojis strategically",
            "Include save-worthy content",
            "Create shareable graphics",
            "Use Instagram-specific features (polls, questions)",
            "Post 1-2 times daily for optimal reach"
        ],
        "content_types": ["Educational carousels", "Behind-the-scenes", "Client testimonials", "Quick tips", "Infographics", "Day-in-the-life"]
    },
    "TikTok": {
        "max_chars": 300,
        "hashtags": 5,
        "tone": "Casual, entertaining, educational",
        "format": "Short-form video (15-60 seconds optimal)",
        "best_practices": [
            "Hook viewers in the first 3 seconds",
            "Use trending sounds and effects",
            "Keep it authentic and relatable",
            "Add captions for accessibility",
            "End with a question or CTA",
            "Post 1-3 times daily"
        ],
        "content_types": ["Quick tips", "Myth-busting", "Day-in-the-life", "Trending challenges", "Educational content", "Q&A responses"]
    },
    "YouTube": {
        "max_chars": 5000,
        "hashtags": 3,
        "tone": "Educational, authoritative, engaging",
        "format": "Long-form videos, Shorts, tutorials",
        "best_practices": [
            "Optimize title with keywords",
            "Create compelling thumbnails",
            "Include timestamps for long videos",
            "Add end screens and cards",
            "Write detailed descriptions with keywords",
            "Engage with comments"
        ],
        "content_types": ["Tutorials", "Case studies", "Webinars", "Product demos", "Expert interviews", "Industry updates"]
    },
    "Twitter/X": {
        "max_chars": 280,
        "hashtags": 2,
        "tone": "Conversational, timely, engaging",
        "format": "Threads, single tweets, polls",
        "best_practices": [
            "Keep tweets concise and punchy",
            "Use threads for longer content",
            "Engage with trending topics",
            "Reply to relevant conversations",
            "Use polls for engagement",
            "Post multiple times daily"
        ],
        "content_types": ["Quick insights", "Industry news commentary", "Threads", "Polls", "Quotes", "Live event coverage"]
    },
    "Facebook": {
        "max_chars": 63206,
        "hashtags": 3,
        "tone": "Community-focused, informative, personable",
        "format": "Posts, videos, events, groups",
        "best_practices": [
            "Create shareable content",
            "Use Facebook Live for engagement",
            "Build and engage with groups",
            "Post native video content",
            "Use Facebook Events for webinars",
            "Respond to comments promptly"
        ],
        "content_types": ["Community updates", "Live videos", "Event promotions", "Educational posts", "Client stories", "Behind-the-scenes"]
    }
}

# Content types and templates - Marketing focused for LawTrax
CONTENT_TYPES = {
    "Marketing - Product Launch": "Announce new features, updates, or capabilities to generate excitement and leads",
    "Marketing - Lead Generation": "Create compelling content designed to capture leads and drive demo requests",
    "Marketing - Brand Awareness": "Build recognition and trust for LawTrax in the immigration law market",
    "Marketing - Competitive Positioning": "Highlight advantages over competitors like INSZoom, Docketwise, LawLogix",
    "Marketing - Case Study/ROI": "Share client success stories with specific metrics (30%+ revenue increase)",
    "Marketing - Demo/Trial Promotion": "Drive sign-ups for demos and free trials",
    "Educational Post": "Create informative content about immigration processes and software benefits",
    "Success Story": "Share client success stories and testimonials that demonstrate value",
    "Product Feature Spotlight": "Highlight specific features like real-time reporting, PDF generation, API access",
    "Industry News Commentary": "Provide expert commentary on USCIS updates, immigration law changes",
    "Tips & Best Practices": "Share actionable tips for immigration professionals",
    "Behind-the-Scenes": "Show company culture, team, and development process",
    "Comparison Post": "Compare LawTrax vs competitors (INSZoom, Docketwise, CampLegal)",
    "FAQ Content": "Address common questions about immigration case management software",
    "Announcement": "Share company news, updates, or launches",
    "Engagement Post": "Create interactive content to boost engagement",
    "Thought Leadership": "Position LawTrax as industry experts in immigration technology",
    "Pain Point Solution": "Address specific challenges law firms face and how LawTrax solves them"
}

# Target Personas for Immigration Law Marketing
TARGET_PERSONAS = {
    "Managing Partner - Large Law Firm": {
        "description": "Decision maker at firms with 50+ attorneys, focuses on ROI, scalability, enterprise features",
        "pain_points": ["Scalability concerns", "Integration with existing systems", "Compliance requirements", "Staff productivity"],
        "motivators": ["Revenue growth", "Competitive advantage", "Risk mitigation", "Operational efficiency"],
        "tone": "Executive, data-driven, ROI-focused",
        "content_focus": "Enterprise features, security, compliance, client success metrics"
    },
    "Immigration Practice Lead": {
        "description": "Heads immigration department, concerned with team efficiency and case outcomes",
        "pain_points": ["Case tracking complexity", "Document management chaos", "Deadline management", "Team coordination"],
        "motivators": ["Streamlined workflows", "Better client service", "Reduced errors", "Team productivity"],
        "tone": "Professional, solution-oriented, practical",
        "content_focus": "Workflow automation, case management, reporting capabilities"
    },
    "Solo Immigration Attorney": {
        "description": "Independent practitioner handling all aspects, needs affordable all-in-one solution",
        "pain_points": ["Limited time", "Wearing multiple hats", "Budget constraints", "Keeping up with forms"],
        "motivators": ["Time savings", "Affordable pricing", "Easy to use", "All-in-one solution"],
        "tone": "Relatable, practical, cost-conscious",
        "content_focus": "Ease of use, time savings, affordable pricing, USCIS form automation"
    },
    "Paralegal/Legal Assistant": {
        "description": "Day-to-day user handling case preparation, document collection, client communication",
        "pain_points": ["Manual data entry", "Chasing documents", "Status update requests", "Form errors"],
        "motivators": ["Automation", "Client portal", "Document management", "Error reduction"],
        "tone": "Practical, feature-focused, user-friendly",
        "content_focus": "Daily workflow features, client portal, document management, automation"
    },
    "Corporate Immigration Manager": {
        "description": "In-house immigration lead at corporations managing employee visas",
        "pain_points": ["Vendor management", "Compliance tracking", "Reporting to leadership", "Employee experience"],
        "motivators": ["Visibility", "Compliance", "Employee satisfaction", "Cost control"],
        "tone": "Corporate, compliance-focused, metrics-driven",
        "content_focus": "Employer portal, reporting, compliance tracking, API integrations"
    },
    "Law Firm IT/Operations": {
        "description": "Technical decision maker concerned with security, integrations, and implementation",
        "pain_points": ["Security concerns", "Integration complexity", "Data migration", "User adoption"],
        "motivators": ["Security certifications", "Easy integration", "Reliable uptime", "Support quality"],
        "tone": "Technical, security-focused, detail-oriented",
        "content_focus": "Security features, API capabilities, cloud infrastructure, compliance certifications"
    }
}

def get_claude_response(prompt, api_key):
    """Generate content using Claude API"""
    try:
        client = anthropic.Anthropic(api_key=api_key)
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4096,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return message.content[0].text
    except anthropic.AuthenticationError:
        return "ERROR: Invalid API key. Please check your Claude API key."
    except anthropic.RateLimitError:
        return "ERROR: Rate limit exceeded. Please wait a moment and try again."
    except Exception as e:
        return f"ERROR: {str(e)}"

def build_content_prompt(company_info, platform, content_type, topic, additional_context, tone, target_audience):
    """Build a comprehensive prompt for content generation"""
    guidelines = PLATFORM_GUIDELINES.get(platform, PLATFORM_GUIDELINES["LinkedIn"])
    
    prompt = f"""You are an expert social media content strategist and copywriter specializing in B2B SaaS marketing for the legal technology industry.

COMPANY INFORMATION:
{company_info}

PLATFORM: {platform}
CONTENT TYPE: {content_type}
TOPIC/THEME: {topic}

PLATFORM SPECIFICATIONS:
- Maximum Characters: {guidelines['max_chars']}
- Recommended Hashtags: {guidelines['hashtags']}
- Tone: {guidelines['tone']}
- Format: {guidelines['format']}

BEST PRACTICES FOR {platform.upper()}:
{chr(10).join(['- ' + bp for bp in guidelines['best_practices']])}

TARGET AUDIENCE: {target_audience}
DESIRED TONE: {tone}

ADDITIONAL CONTEXT/REQUIREMENTS:
{additional_context if additional_context else 'None specified'}

TASK:
Create a compelling {content_type.lower()} for {platform} about "{topic}".

The content should:
1. Be optimized for {platform}'s algorithm and best practices
2. Include a strong hook/opening
3. Provide genuine value to the target audience
4. Include a clear call-to-action
5. Be formatted appropriately for the platform
6. Include relevant hashtags (exact number: {guidelines['hashtags']})
7. Stay within character limits

OUTPUT FORMAT:
Provide the ready-to-post content with:
1. MAIN CONTENT (the actual post text)
2. HASHTAGS (platform-appropriate)
3. POSTING TIPS (2-3 specific tips for this post)
4. BEST TIME TO POST (recommended timing)
5. SUGGESTED VISUAL (description of ideal accompanying image/video)

Make the content engaging, authentic, and aligned with the company's voice while following all platform best practices."""

    return prompt

def build_video_script_prompt(company_info, platform, video_type, topic, duration, additional_context):
    """Build prompt for video script generation"""
    prompt = f"""You are an expert video content strategist and scriptwriter specializing in B2B SaaS marketing for the legal technology industry.

COMPANY INFORMATION:
{company_info}

PLATFORM: {platform}
VIDEO TYPE: {video_type}
TOPIC: {topic}
TARGET DURATION: {duration}

ADDITIONAL CONTEXT:
{additional_context if additional_context else 'None specified'}

TASK:
Create a complete video script for a {video_type} about "{topic}" for {platform}.

The script should include:

1. HOOK (First 3 seconds) - Attention-grabbing opening
2. INTRO (5-10 seconds) - Brief context setting
3. MAIN CONTENT - Structured body with clear sections
4. CALL TO ACTION - What viewers should do next
5. OUTRO - Memorable closing

OUTPUT FORMAT:
Provide a complete script with:
1. FULL SCRIPT (with timestamps and speaker directions)
2. B-ROLL SUGGESTIONS (visual elements to include)
3. ON-SCREEN TEXT/GRAPHICS (key points to display)
4. MUSIC/SOUND RECOMMENDATIONS
5. THUMBNAIL CONCEPT (for YouTube/TikTok)
6. CAPTION/DESCRIPTION (for posting)
7. HASHTAGS (platform-appropriate)

Make it engaging, informative, and optimized for {platform}'s algorithm."""

    return prompt

def build_seo_content_prompt(company_info, content_type, primary_keyword, secondary_keywords, target_word_count, additional_context):
    """Build prompt for SEO-optimized content"""
    prompt = f"""You are an expert SEO content strategist and writer specializing in B2B SaaS marketing for the legal technology industry.

COMPANY INFORMATION:
{company_info}

CONTENT TYPE: {content_type}
PRIMARY KEYWORD: {primary_keyword}
SECONDARY KEYWORDS: {secondary_keywords}
TARGET WORD COUNT: {target_word_count}

ADDITIONAL CONTEXT:
{additional_context if additional_context else 'None specified'}

TASK:
Create SEO-optimized content for "{primary_keyword}".

The content should:
1. Naturally incorporate the primary keyword in title, headers, and body
2. Include secondary keywords throughout
3. Follow on-page SEO best practices
4. Provide genuine value to readers
5. Include internal linking opportunities
6. Be structured with proper H1, H2, H3 hierarchy

OUTPUT FORMAT:
Provide complete content with:
1. META TITLE (50-60 characters)
2. META DESCRIPTION (150-160 characters)
3. FULL CONTENT (with proper heading structure)
4. KEYWORD DENSITY ANALYSIS
5. INTERNAL LINKING SUGGESTIONS
6. FEATURED SNIPPET OPTIMIZATION (structured for position zero)
7. FAQ SECTION (for additional keyword targeting)
8. SCHEMA MARKUP SUGGESTIONS

Make it comprehensive, authoritative, and optimized for search intent."""

    return prompt

# Sidebar
with st.sidebar:
    st.markdown("""
    <div class="sidebar-header">
        <h2>🚀 Marketing Command Center</h2>
        <p>Powered by AI</p>
    </div>
    """, unsafe_allow_html=True)
    
    # API Key Input
    st.markdown("### 🔑 API Configuration")
    
    # Check if API key is already loaded from secrets
    if st.session_state.api_key:
        st.success("✅ API Key loaded from secrets")
        # Option to override
        override_key = st.checkbox("Override API Key", value=False)
        if override_key:
            api_key = st.text_input(
                "Enter New API Key",
                type="password",
                help="Enter your Anthropic Claude API key to override"
            )
            if api_key:
                st.session_state.api_key = api_key
                st.success("✅ API Key updated")
    else:
        api_key = st.text_input(
            "Claude API Key",
            type="password",
            value="",
            help="Enter your Anthropic Claude API key (or add CLAUDE_API_KEY to secrets.toml)"
        )
        if api_key:
            st.session_state.api_key = api_key
            st.success("✅ API Key configured")
        else:
            st.warning("⚠️ Add CLAUDE_API_KEY to secrets.toml or enter below")
    
    st.divider()
    
    # Feature Controls - Token Management
    st.markdown("### ⚙️ Feature Controls")
    st.caption("Disable features to save API tokens")
    
    enable_video_scripts = st.checkbox(
        "🎬 Enable Video Scripts",
        value=False,
        help="Enable/disable video script generation (uses tokens)"
    )
    
    enable_video_generation = st.checkbox(
        "🎥 Enable Video Generation",
        value=False,
        help="Enable/disable AI video generation packages (uses tokens)"
    )
    
    enable_seo_content = st.checkbox(
        "🔍 Enable SEO Content",
        value=True,
        help="Enable/disable SEO content generation"
    )
    
    enable_social_media = st.checkbox(
        "📱 Enable Social Media",
        value=True,
        help="Enable/disable social media content generation"
    )
    
    # Store in session state
    st.session_state.enable_video_scripts = enable_video_scripts
    st.session_state.enable_video_generation = enable_video_generation
    st.session_state.enable_seo_content = enable_seo_content
    st.session_state.enable_social_media = enable_social_media
    
    if not enable_video_scripts and not enable_video_generation:
        st.info("💰 Video features disabled - saving tokens!")
    
    st.divider()
    
    # Company Configuration
    st.markdown("### 🏢 Company Profile")
    use_default = st.checkbox("Use LawTrax (Default)", value=True)
    
    if not use_default:
        company_name = st.text_input("Company Name", placeholder="Enter company name")
        company_description = st.text_area(
            "Company Description",
            placeholder="Describe your company, products, and value proposition...",
            height=150
        )
        company_website = st.text_input("Website", placeholder="https://example.com")
        target_market = st.text_input("Target Market", placeholder="e.g., Immigration law firms")
        key_features = st.text_area(
            "Key Features/Benefits",
            placeholder="List your main features and benefits...",
            height=100
        )
        
        if company_name and company_description:
            st.session_state.company_profile = {
                "name": company_name,
                "description": company_description,
                "website": company_website,
                "target_market": target_market,
                "features": key_features
            }
    
    st.divider()
    
    # Quick Stats
    st.markdown("### 📊 Session Stats")
    st.metric("Content Generated", len(st.session_state.generated_content))
    
    if st.button("🗑️ Clear History"):
        st.session_state.generated_content = []
        st.rerun()

# Main Header
st.markdown("""
<div class="main-header">
    <h1>🚀 Marketing Command Center</h1>
    <p>AI-Powered Content Generation for Immigration Software Marketing</p>
</div>
""", unsafe_allow_html=True)

# Get company info
if use_default:
    company_info = LAWTRAX_KNOWLEDGE
    company_display_name = "LawTrax"
else:
    if st.session_state.company_profile:
        profile = st.session_state.company_profile
        company_info = f"""
COMPANY: {profile.get('name', 'N/A')}
WEBSITE: {profile.get('website', 'N/A')}
DESCRIPTION: {profile.get('description', 'N/A')}
TARGET MARKET: {profile.get('target_market', 'N/A')}
KEY FEATURES: {profile.get('features', 'N/A')}
"""
        company_display_name = profile.get('name', 'Your Company')
    else:
        company_info = "No company profile configured. Please set up in sidebar."
        company_display_name = "Your Company"

# Main Tabs
tab0, tab1, tab2, tab2b, tab3, tab4, tab5 = st.tabs([
    "🏠 LawTrax Overview",
    "📱 Social Media Content",
    "🎬 Video Scripts",
    "🎥 Generate Videos",
    "🔍 SEO Content",
    "📚 Knowledge Base",
    "📋 Content History"
])

# Tab 0: LawTrax Overview (Landing Page)
with tab0:
    st.markdown("""
    <div style="text-align: center; padding: 1rem 0;">
        <h1 style="color: #4B0082; font-size: 3rem; margin-bottom: 0;">LAWTRAX</h1>
        <p style="font-size: 1.5rem; color: #666; margin-top: 0;">Immigration Software for the Modern Attorney</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Hero Section
    st.markdown("""
    <div style="background: linear-gradient(135deg, #4B0082 0%, #7B68EE 50%, #9370DB 100%); 
                padding: 2.5rem; border-radius: 20px; color: white; margin-bottom: 2rem;
                box-shadow: 0 10px 40px rgba(75, 0, 130, 0.3);">
        <h2 style="margin-bottom: 1rem; font-size: 1.8rem;">🚀 The Only Cloud-Based Digital Attorney Platform You Need</h2>
        <p style="font-size: 1.1rem; line-height: 1.8; opacity: 0.95;">
            LawTrax empowers immigration attorney firms with a secure, all-in-one platform to manage leads, clients, 
            and cases effortlessly. Customize workflows to fit your business needs, seamlessly integrate carrier label 
            generation and invoice management, and maximize efficiency with our streamlined solution.
        </p>
        <div style="margin-top: 1.5rem; display: flex; gap: 1rem; flex-wrap: wrap;">
            <span style="background: rgba(255,255,255,0.2); padding: 0.5rem 1rem; border-radius: 20px;">✅ 30%+ Revenue Increase</span>
            <span style="background: rgba(255,255,255,0.2); padding: 0.5rem 1rem; border-radius: 20px;">✅ 99.9% Uptime</span>
            <span style="background: rgba(255,255,255,0.2); padding: 0.5rem 1rem; border-radius: 20px;">✅ Real-Time Reporting</span>
            <span style="background: rgba(255,255,255,0.2); padding: 0.5rem 1rem; border-radius: 20px;">✅ Zero API Costs</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Key Metrics
    st.markdown("### 📊 Platform Impact")
    metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
    with metric_col1:
        st.metric("Revenue Increase", "30%+", "Client Reported")
    with metric_col2:
        st.metric("Platform Uptime", "99.9%", "Google Cloud")
    with metric_col3:
        st.metric("Report Delay", "0 hrs", "vs 24hr industry avg")
    with metric_col4:
        st.metric("API Cost", "$0", "Included Free")
    
    st.markdown("---")
    
    # Core Platform Features
    st.markdown("### 🎯 Core Platform Features")
    
    feature_col1, feature_col2 = st.columns(2)
    
    with feature_col1:
        st.markdown("""
        <div style="background: white; padding: 1.5rem; border-radius: 15px; margin-bottom: 1rem; 
                    border-left: 5px solid #4B0082; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
            <h4 style="color: #4B0082; margin-bottom: 0.5rem;">📋 Case Management</h4>
            <p style="color: #555; margin: 0;">Workflow-based platform with multiple stages based on case type. 
            End-to-end management, tracking, assigning, and real-time stakeholder notifications. 
            Business rules ensure all required documents are captured and verified before completion.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="background: white; padding: 1.5rem; border-radius: 15px; margin-bottom: 1rem; 
                    border-left: 5px solid #7B68EE; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
            <h4 style="color: #7B68EE; margin-bottom: 0.5rem;">👥 Customer Management</h4>
            <p style="color: #555; margin: 0;">Secure cloud portal for companies and beneficiaries to manage 
            information and initiate cases with a single click. Complete automation from attorney assignment 
            to case completion based on provided data.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="background: white; padding: 1.5rem; border-radius: 15px; margin-bottom: 1rem; 
                    border-left: 5px solid #9370DB; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
            <h4 style="color: #9370DB; margin-bottom: 0.5rem;">🎯 Lead Management</h4>
            <p style="color: #555; margin: 0;">Built-in CRM to convert prospects into customers. Track leads 
            at various conversion stages with recorded interactions. Categorize as potential or hot leads 
            with dedicated team assignment for tracking and closure.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="background: white; padding: 1.5rem; border-radius: 15px; margin-bottom: 1rem; 
                    border-left: 5px solid #32CD32; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
            <h4 style="color: #32CD32; margin-bottom: 0.5rem;">📄 Document Management</h4>
            <p style="color: #555; margin: 0;">Cloud-based, indexable, searchable system with three stages: 
            identification, generation, and delivery. Documents merged into single PDF per visa type. 
            Complete audit trail for all uploads, edits, assignments, and deletions.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with feature_col2:
        st.markdown("""
        <div style="background: white; padding: 1.5rem; border-radius: 15px; margin-bottom: 1rem; 
                    border-left: 5px solid #FF6B6B; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
            <h4 style="color: #FF6B6B; margin-bottom: 0.5rem;">📊 Dashboard & Reporting</h4>
            <p style="color: #555; margin: 0;">Real-time business-driven dashboards with drill-down capabilities. 
            Configurable KPIs with drag-and-drop functionality. Comprehensive reporting for decision-making 
            with customizable branded reports.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="background: white; padding: 1.5rem; border-radius: 15px; margin-bottom: 1rem; 
                    border-left: 5px solid #4ECDC4; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
            <h4 style="color: #4ECDC4; margin-bottom: 0.5rem;">📝 PDF Generation</h4>
            <p style="color: #555; margin: 0;">Auto-generate USCIS and DoL formatted documents based on case type rules. 
            Identifies case type, collates required data, and generates submission-ready documents 
            following all visa-specific conditions.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="background: white; padding: 1.5rem; border-radius: 15px; margin-bottom: 1rem; 
                    border-left: 5px solid #FFE66D; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
            <h4 style="color: #E6B800; margin-bottom: 0.5rem;">🌐 Client Portal</h4>
            <p style="color: #555; margin: 0;">Secure document uploads and case status tracking for clients. 
            Automated notifications on case updates. Exclusive cloud portal for companies to manage 
            information and initiate beneficiary cases.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="background: white; padding: 1.5rem; border-radius: 15px; margin-bottom: 1rem; 
                    border-left: 5px solid #96CEB4; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
            <h4 style="color: #96CEB4; margin-bottom: 0.5rem;">🔗 Integrations</h4>
            <p style="color: #555; margin: 0;">Outlook integration for meetings, appointments, and case alerts. 
            QuickBooks billing system integration. Webhooks and RESTful APIs for third-party integrations 
            with no additional costs.</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Security & Compliance
    st.markdown("### 🔒 Enterprise Security & Compliance")
    
    sec_col1, sec_col2, sec_col3 = st.columns(3)
    
    with sec_col1:
        st.markdown("""
        <div style="background: linear-gradient(145deg, #f8f9fa 0%, #e9ecef 100%); 
                    padding: 1.5rem; border-radius: 15px; text-align: center; height: 200px;">
            <div style="font-size: 3rem; margin-bottom: 0.5rem;">🛡️</div>
            <h4 style="color: #4B0082;">Infrastructure Security</h4>
            <p style="color: #666; font-size: 0.9rem;">
                Multi-tenant SaaS on Google Cloud Platform with Firebase. 
                Broker patterns for tenant isolation. 99.9% uptime guarantee.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with sec_col2:
        st.markdown("""
        <div style="background: linear-gradient(145deg, #f8f9fa 0%, #e9ecef 100%); 
                    padding: 1.5rem; border-radius: 15px; text-align: center; height: 200px;">
            <div style="font-size: 3rem; margin-bottom: 0.5rem;">🔐</div>
            <h4 style="color: #4B0082;">Data Protection</h4>
            <p style="color: #666; font-size: 0.9rem;">
                End-to-end encryption at rest and in transit. Each client has own instance. 
                Digital tokens for API authentication.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with sec_col3:
        st.markdown("""
        <div style="background: linear-gradient(145deg, #f8f9fa 0%, #e9ecef 100%); 
                    padding: 1.5rem; border-radius: 15px; text-align: center; height: 200px;">
            <div style="font-size: 3rem; margin-bottom: 0.5rem;">✅</div>
            <h4 style="color: #4B0082;">Compliance Ready</h4>
            <p style="color: #666; font-size: 0.9rem;">
                SOC 2 Type II • GDPR • HIPAA Compliant • CCPA • PCI Compliance • 
                Role-based access with SSO support.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Competitive Advantages
    st.markdown("### 💪 Why Choose LawTrax Over Competitors?")
    
    st.markdown("""
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1rem;">
        <div style="background: #e8f5e9; padding: 1.5rem; border-radius: 12px; border-left: 4px solid #4CAF50;">
            <h4 style="color: #2E7D32; margin: 0 0 0.5rem 0;">✅ No Additional API Costs</h4>
            <p style="margin: 0; color: #555;">Unlike competitors who charge extra for API access, 
            LawTrax includes full API capabilities at no additional cost.</p>
        </div>
        <div style="background: #e3f2fd; padding: 1.5rem; border-radius: 12px; border-left: 4px solid #2196F3;">
            <h4 style="color: #1565C0; margin: 0 0 0.5rem 0;">✅ True Real-Time Reporting</h4>
            <p style="margin: 0; color: #555;">No 24-hour batch delays. Get instant access to your data 
            when you need it for client support and decision making.</p>
        </div>
        <div style="background: #fff3e0; padding: 1.5rem; border-radius: 12px; border-left: 4px solid #FF9800;">
            <h4 style="color: #E65100; margin: 0 0 0.5rem 0;">✅ Google Cloud Infrastructure</h4>
            <p style="margin: 0; color: #555;">Enterprise-grade 99.9% uptime guarantee backed by 
            Google's world-class infrastructure and security.</p>
        </div>
        <div style="background: #f3e5f5; padding: 1.5rem; border-radius: 12px; border-left: 4px solid #9C27B0;">
            <h4 style="color: #7B1FA2; margin: 0 0 0.5rem 0;">✅ Built-in USCIS/DoL Generator</h4>
            <p style="margin: 0; color: #555;">Automatic PDF generation in proper government format 
            with business rules for each visa type.</p>
        </div>
        <div style="background: #ffebee; padding: 1.5rem; border-radius: 12px; border-left: 4px solid #f44336;">
            <h4 style="color: #C62828; margin: 0 0 0.5rem 0;">✅ Complete Audit Trail</h4>
            <p style="margin: 0; color: #555;">Every action is logged for compliance. Know who did what 
            and when across every case and document.</p>
        </div>
        <div style="background: #e0f7fa; padding: 1.5rem; border-radius: 12px; border-left: 4px solid #00BCD4;">
            <h4 style="color: #00838F; margin: 0 0 0.5rem 0;">✅ 25+ Years Experience</h4>
            <p style="margin: 0; color: #555;">Built by experts with collective 25+ years in immigration 
            law technology and digital processing.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Target Market
    st.markdown("### 🎯 Who Uses LawTrax?")
    
    market_col1, market_col2, market_col3, market_col4 = st.columns(4)
    
    with market_col1:
        st.markdown("""
        <div style="text-align: center; padding: 1rem;">
            <div style="font-size: 3rem;">⚖️</div>
            <h4 style="color: #4B0082;">Immigration Law Firms</h4>
            <p style="color: #666; font-size: 0.85rem;">Solo practitioners to large enterprises</p>
        </div>
        """, unsafe_allow_html=True)
    
    with market_col2:
        st.markdown("""
        <div style="text-align: center; padding: 1rem;">
            <div style="font-size: 3rem;">🏢</div>
            <h4 style="color: #4B0082;">Corporate Immigration</h4>
            <p style="color: #666; font-size: 0.85rem;">In-house immigration departments</p>
        </div>
        """, unsafe_allow_html=True)
    
    with market_col3:
        st.markdown("""
        <div style="text-align: center; padding: 1rem;">
            <div style="font-size: 3rem;">🌍</div>
            <h4 style="color: #4B0082;">Global Mobility Teams</h4>
            <p style="color: #666; font-size: 0.85rem;">International workforce management</p>
        </div>
        """, unsafe_allow_html=True)
    
    with market_col4:
        st.markdown("""
        <div style="text-align: center; padding: 1rem;">
            <div style="font-size: 3rem;">🤝</div>
            <h4 style="color: #4B0082;">Legal Service Providers</h4>
            <p style="color: #666; font-size: 0.85rem;">Immigration-focused legal services</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Client Testimonial
    st.markdown("### 💬 Client Success Story")
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 2rem; border-radius: 15px; color: white; margin: 1rem 0;">
        <div style="font-size: 3rem; opacity: 0.3; margin-bottom: -1rem;">❝</div>
        <p style="font-size: 1.2rem; line-height: 1.8; font-style: italic;">
            "LawTrax has helped us put the customer's interests first and focus on cases and interactions 
            rather than operations and paperwork. We realized that we could handle more cases than we were 
            managing, resulting in an <strong>increase in our revenue of at least 30%</strong>. I highly recommend 
            this tool for attorneys and firms looking to improve productivity."
        </p>
        <p style="margin-top: 1rem; font-weight: bold;">— Immigration Law Firm Client</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Contact Information
    st.markdown("### 📞 Get Started with LawTrax")
    
    contact_col1, contact_col2, contact_col3 = st.columns(3)
    
    with contact_col1:
        st.markdown("""
        <div style="background: #f8f9fa; padding: 1.5rem; border-radius: 12px; text-align: center;">
            <div style="font-size: 2rem;">📧</div>
            <h4>Email Us</h4>
            <p style="color: #4B0082; font-weight: bold;">info@lawtrax.com</p>
        </div>
        """, unsafe_allow_html=True)
    
    with contact_col2:
        st.markdown("""
        <div style="background: #f8f9fa; padding: 1.5rem; border-radius: 12px; text-align: center;">
            <div style="font-size: 2rem;">📱</div>
            <h4>Call Us</h4>
            <p style="color: #4B0082; font-weight: bold;">972-200-1030</p>
        </div>
        """, unsafe_allow_html=True)
    
    with contact_col3:
        st.markdown("""
        <div style="background: #f8f9fa; padding: 1.5rem; border-radius: 12px; text-align: center;">
            <div style="font-size: 2rem;">🌐</div>
            <h4>Visit Website</h4>
            <p style="color: #4B0082; font-weight: bold;">lawtrax.com</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="text-align: center; margin-top: 1rem; color: #666;">
        <p>📍 17400 Dallas Parkway, Suite 121, Dallas, Texas 75287</p>
    </div>
    """, unsafe_allow_html=True)
    
    # CTA
    st.markdown("""
    <div style="background: linear-gradient(135deg, #4B0082 0%, #7B68EE 100%); 
                padding: 2rem; border-radius: 15px; text-align: center; margin-top: 2rem;">
        <h3 style="color: white; margin-bottom: 1rem;">Ready to Transform Your Immigration Practice?</h3>
        <p style="color: rgba(255,255,255,0.9); margin-bottom: 1.5rem;">
            Use the tabs above to generate marketing content, or visit lawtrax.com to schedule a demo!
        </p>
    </div>
    """, unsafe_allow_html=True)

# Tab 1: Social Media Content
with tab1:
    st.markdown("## 📱 Social Media Content Generator")
    st.markdown(f"Creating **marketing content** for **{company_display_name}** to reach immigration law professionals")
    
    # Marketing Goal Selection
    st.markdown("### 🎯 Marketing Objective")
    marketing_goal = st.selectbox(
        "What's your primary goal?",
        [
            "Generate Leads & Demo Requests",
            "Build Brand Awareness",
            "Showcase Product Features",
            "Share Client Success Stories",
            "Establish Thought Leadership",
            "Drive Website Traffic",
            "Promote Special Offers/Trials",
            "Compete Against Alternatives"
        ],
        help="Select your primary marketing objective for this content"
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        platform = st.selectbox(
            "Select Platform",
            list(PLATFORM_GUIDELINES.keys()),
            help="Choose the social media platform"
        )
        
        content_type = st.selectbox(
            "Content Type",
            list(CONTENT_TYPES.keys()),
            help="Select the type of content to create"
        )
        st.caption(f"💡 {CONTENT_TYPES[content_type]}")
        
        topic = st.text_input(
            "Topic/Theme",
            placeholder="e.g., How LawTrax reduces H-1B processing time by 50%",
            help="What should the post be about?"
        )
    
    with col2:
        # Persona Selection
        target_persona = st.selectbox(
            "🎯 Target Persona",
            list(TARGET_PERSONAS.keys()),
            help="Select who you're targeting with this content"
        )
        
        persona_info = TARGET_PERSONAS[target_persona]
        st.markdown(f"""
        <div style="background: #f0f4f8; padding: 1rem; border-radius: 8px; font-size: 0.85rem;">
            <strong>Persona Profile:</strong><br>
            {persona_info['description']}<br><br>
            <strong>Key Pain Points:</strong> {', '.join(persona_info['pain_points'][:2])}<br>
            <strong>Recommended Tone:</strong> {persona_info['tone']}
        </div>
        """, unsafe_allow_html=True)
        
        tone = st.selectbox(
            "Tone",
            ["Professional & Authoritative", "Conversational & Relatable", "Educational & Helpful", 
             "Urgent & Action-Oriented", "Inspiring & Visionary", "Data-Driven & ROI-Focused",
             "Friendly & Approachable", "Technical & Detailed"],
            help="Select the desired tone"
        )
    
    # Additional targeting options
    st.markdown("### 📝 Content Details")
    detail_col1, detail_col2 = st.columns(2)
    
    with detail_col1:
        include_cta = st.selectbox(
            "Call-to-Action Type",
            [
                "Book a Demo",
                "Start Free Trial",
                "Learn More (Website)",
                "Download Resource",
                "Contact Sales",
                "Watch Video Demo",
                "Read Case Study",
                "Get Pricing",
                "Join Webinar",
                "Comment Below (Engagement)",
                "No CTA (Awareness Only)"
            ]
        )
        
        # LinkedIn-specific hook selector
        if platform == "LinkedIn":
            hook_style = st.selectbox(
                "🎣 Hook Style",
                [
                    "Auto-Generate Best Hook",
                    "Lessons Learned: 'I spent X years doing Y. Here's what I learned:'",
                    "Contrarian: 'Stop doing X. Do this instead:'",
                    "Hot Take: '[Unpopular opinion]. Here's why:'",
                    "Mistake Alert: 'The biggest mistake I see [persona] make:'",
                    "Listicle: '[Number] things that will [benefit]:'",
                    "Story: 'I was wrong about X. Here's the truth:'",
                    "Direct Address: '[Persona], you need to hear this:'",
                    "Curiosity Gap: 'Most people don't know this about [topic]...'",
                    "Results: 'This changed everything for our clients:'"
                ],
                help="Select a proven hook format for higher engagement"
            )
        else:
            hook_style = "Auto-Generate Best Hook"
        
        competitor_mention = st.multiselect(
            "Competitors to Position Against (Optional)",
            ["INSZoom", "Docketwise", "LawLogix Edge", "CampLegal", "Clio", "MyCase", "Generic Spreadsheets"],
            help="Select if you want to subtly position against competitors"
        )
    
    with detail_col2:
        key_features = st.multiselect(
            "Key Features to Highlight",
            [
                "Real-Time Reporting (No 24hr Delays)",
                "Zero Additional API Costs",
                "99.9% Uptime Guarantee",
                "Built-in USCIS/DoL PDF Generator",
                "Secure Client Portal",
                "Complete Audit Trail",
                "QuickBooks Integration",
                "Outlook Calendar Sync",
                "Lead Management CRM",
                "Document Management System",
                "Automated Notifications",
                "Custom Workflows",
                "30%+ Revenue Increase Results"
            ],
            help="Select features to emphasize in the content"
        )
        
        additional_context = st.text_area(
            "Additional Context (Optional)",
            placeholder="Any specific points, current promotions, or requirements...",
            height=80
        )
    
    # Platform-specific info
    guidelines = PLATFORM_GUIDELINES.get(platform, {})
    
    # Special LinkedIn tips section
    if platform == "LinkedIn":
        st.markdown("""
        <div style="background: linear-gradient(135deg, #0077B5 0%, #00A0DC 100%); 
                    padding: 1.5rem; border-radius: 12px; color: white; margin-bottom: 1rem;">
            <h4 style="margin: 0 0 1rem 0;">🔥 LinkedIn Viral Post Formula</h4>
            <p style="margin: 0; font-size: 0.95rem; line-height: 1.6;">
                <strong>Hook Examples That Work:</strong><br>
                • "I've helped 50+ immigration firms. Here's what the top 1% do differently:"<br>
                • "Stop using spreadsheets for case management. Here's why:"<br>
                • "Most immigration attorneys waste 10+ hours/week on admin. The solution?"<br>
                • "Unpopular opinion: Your case management software is killing your revenue."<br><br>
                <strong>Format Rules:</strong> One sentence per line → Blank lines between → Hook first → Question at end → Hashtags last
            </p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="info-box">
            <strong>📌 {platform} Guidelines:</strong><br>
            • Max Characters: {guidelines.get('max_chars', 'N/A')} | Hashtags: {guidelines.get('hashtags', 'N/A')}<br>
            • Tone: {guidelines.get('tone', 'N/A')}<br>
            • Best Formats: {guidelines.get('format', 'N/A')}
        </div>
        """, unsafe_allow_html=True)
    
    # Check if social media is enabled
    social_media_enabled = st.session_state.get('enable_social_media', True)
    
    if not social_media_enabled:
        st.warning("⚠️ **Social Media Content Generation is DISABLED**. Enable in sidebar → '📱 Enable Social Media'")
    
    if st.button("✨ Generate Marketing Content", type="primary", use_container_width=True, disabled=not social_media_enabled):
        if not st.session_state.api_key:
            st.error("⚠️ Please enter your Claude API key in the sidebar")
        elif not topic:
            st.error("⚠️ Please enter a topic")
        else:
            with st.spinner(f"🎨 Creating {platform} marketing content..."):
                # Build enhanced marketing prompt
                persona_details = TARGET_PERSONAS[target_persona]
                
                # Special LinkedIn formatting for viral posts
                if platform == "LinkedIn":
                    enhanced_prompt = f"""You are a TOP LinkedIn content creator and B2B marketing expert who writes viral posts 
that get 100K+ impressions. You understand the LinkedIn algorithm perfectly and write posts that STOP THE SCROLL.

COMPANY INFORMATION:
{company_info}

MARKETING OBJECTIVE: {marketing_goal}

TARGET PERSONA: {target_persona}
- Description: {persona_details['description']}
- Pain Points: {', '.join(persona_details['pain_points'])}
- Motivators: {', '.join(persona_details['motivators'])}

CONTENT TYPE: {content_type}
TOPIC: {topic}
DESIRED TONE: {tone}
CALL-TO-ACTION: {include_cta}
HOOK STYLE PREFERENCE: {hook_style if platform == "LinkedIn" else "N/A"}
KEY FEATURES TO HIGHLIGHT: {', '.join(key_features) if key_features else 'General platform benefits'}
COMPETITORS TO POSITION AGAINST: {', '.join(competitor_mention) if competitor_mention else 'None'}
ADDITIONAL CONTEXT: {additional_context if additional_context else 'None'}

═══════════════════════════════════════════════════════════
CRITICAL LINKEDIN VIRAL POST RULES (FOLLOW EXACTLY):
═══════════════════════════════════════════════════════════

1. **HOOK (First Line)** - This is EVERYTHING. Must create curiosity gap or pattern interrupt.
   Examples of hooks that work:
   - "I've helped 50+ immigration law firms. Here's what the top 1% do differently:"
   - "Stop using spreadsheets for case management. Here's why:"
   - "Most immigration attorneys waste 10+ hours/week on admin. The solution?"
   - "Unpopular opinion: Your case management software is killing your revenue."
   - "I was skeptical about immigration software. Then I saw a firm increase revenue 30%."

2. **FORMAT** - This is non-negotiable:
   - ONE sentence per line
   - Blank line between EVERY sentence
   - Short sentences (under 15 words each)
   - NO long paragraphs ever
   - Use → or • for lists
   - Maximum 1,200-1,500 characters

3. **STRUCTURE**:
   Line 1: HOOK (curiosity/controversy/bold claim)
   Line 2-3: Expand the hook / set up the problem
   Line 4-8: The insight/story/value (one point per line)
   Line 9-10: The solution/revelation
   Line 11: Call-to-action or question
   Line 12: Hashtags (3-5 at very end)

4. **ENGAGEMENT TRIGGERS**:
   - End with a question that's easy to answer
   - Use "you" frequently to speak directly to reader
   - Include a specific number or metric
   - Share a contrarian or surprising insight

5. **WHAT NOT TO DO**:
   - No external links in post body (kills reach)
   - No more than 2-3 emojis total
   - No corporate jargon or buzzwords
   - No long paragraphs
   - No hashtags mixed into the text

═══════════════════════════════════════════════════════════

TASK: Write a VIRAL LinkedIn post about "{topic}" targeting {target_persona}.

OUTPUT FORMAT (Follow this EXACTLY):

---
**📱 LINKEDIN POST (Copy & Paste Ready):**

[Write the complete post here with PERFECT formatting:
- Hook on line 1
- One sentence per line
- Blank lines between sentences
- Question or CTA at end
- Hashtags at very bottom]

---

**🎯 WHY THIS POST WILL PERFORM:**
[2-3 bullet points on why this hooks the target persona]

**⏰ BEST TIME TO POST:**
[Specific day and time recommendation]

**💬 ENGAGEMENT STRATEGY:**
[How to respond to comments to boost reach]

**🔗 COMMENT CTA:**
[What to put in the first comment - usually the link]

**📊 EXPECTED PERFORMANCE:**
[Realistic engagement expectations]

---

Remember: The post MUST look like it was written by a human thought leader, NOT a company. 
First-person, authentic, valuable, and formatted for MOBILE READABILITY."""

                else:
                    # Standard prompt for other platforms
                    enhanced_prompt = f"""You are an expert B2B SaaS marketing strategist specializing in legal technology marketing, 
specifically immigration case management software. You understand the immigration law market deeply.

COMPANY INFORMATION:
{company_info}

MARKETING OBJECTIVE: {marketing_goal}

TARGET PERSONA: {target_persona}
- Description: {persona_details['description']}
- Pain Points: {', '.join(persona_details['pain_points'])}
- Motivators: {', '.join(persona_details['motivators'])}
- Preferred Tone: {persona_details['tone']}
- Content Focus: {persona_details['content_focus']}

PLATFORM: {platform}
CONTENT TYPE: {content_type}
TOPIC: {topic}
DESIRED TONE: {tone}

PLATFORM SPECIFICATIONS:
- Maximum Characters: {guidelines['max_chars']}
- Recommended Hashtags: {guidelines['hashtags']}
- Platform Tone: {guidelines['tone']}
- Format: {guidelines['format']}

CALL-TO-ACTION: {include_cta}
KEY FEATURES TO HIGHLIGHT: {', '.join(key_features) if key_features else 'General platform benefits'}
COMPETITORS TO POSITION AGAINST: {', '.join(competitor_mention) if competitor_mention else 'None - focus on LawTrax strengths'}

ADDITIONAL CONTEXT: {additional_context if additional_context else 'None'}

BEST PRACTICES FOR {platform.upper()}:
{chr(10).join(['- ' + bp for bp in guidelines['best_practices']])}

TASK:
Create compelling marketing content for {platform} that:
1. Speaks directly to the {target_persona} persona's pain points and motivators
2. Achieves the marketing objective: {marketing_goal}
3. Highlights LawTrax's unique value propositions
4. Includes a strong hook that stops the scroll
5. Builds credibility and trust
6. Includes the specified call-to-action: {include_cta}
7. Is optimized for {platform}'s algorithm and best practices
8. Uses social proof and specific metrics where possible (e.g., "30% revenue increase", "99.9% uptime")

OUTPUT FORMAT:
Provide ready-to-post content with:

**📱 MAIN CONTENT:**
[The actual post text, fully formatted for {platform}]

**#️⃣ HASHTAGS:**
[{guidelines['hashtags']} relevant hashtags]

**🎯 TARGETING NOTES:**
[Why this content will resonate with {target_persona}]

**📊 POSTING STRATEGY:**
- Best time to post
- Engagement tips
- Follow-up content ideas

**🖼️ VISUAL SUGGESTION:**
[Description of ideal accompanying image/video/graphic]

**📈 SUCCESS METRICS:**
[What metrics to track for this post]

Make the content compelling, authentic, and designed to generate leads for LawTrax."""

                result = get_claude_response(enhanced_prompt, st.session_state.api_key)
                
                if not result.startswith("ERROR"):
                    st.session_state.generated_content.append({
                        "type": "Social Media Marketing",
                        "platform": platform,
                        "topic": topic,
                        "persona": target_persona,
                        "goal": marketing_goal,
                        "content": result,
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")
                    })
                    
                    st.markdown('<div class="success-banner">✅ Marketing Content Generated!</div>', unsafe_allow_html=True)
                    st.markdown("### 📝 Generated Marketing Content")
                    st.markdown(result)
                    
                    # Copy button
                    st.download_button(
                        label="📥 Download Content",
                        data=result,
                        file_name=f"{platform.lower()}_marketing_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                        mime="text/plain"
                    )
                else:
                    st.error(result)

# Tab 2: Video Scripts & Marketing Videos
with tab2:
    st.markdown("## 🎬 Video Marketing Generator")
    st.markdown(f"Creating **video marketing content** for **{company_display_name}** to drive leads and conversions")
    
    # Check if feature is enabled - show banner if disabled
    if not st.session_state.get('enable_video_scripts', False):
        st.warning("⚠️ **Video Script Generation is DISABLED** to save API tokens. Enable in sidebar → '🎬 Enable Video Scripts'")
    
    # Video Marketing Goal
    st.markdown("### 🎯 Video Marketing Objective")
    video_goal = st.selectbox(
        "What's your video goal?",
        [
            "Generate Demo Requests",
            "Explain Product Benefits",
            "Share Client Success Story",
            "Compare Against Competitors",
            "Address Common Objections",
            "Showcase Specific Feature",
            "Build Brand Awareness",
            "Educate on Immigration Tech",
            "Promote Webinar/Event",
            "Retarget Website Visitors"
        ],
        key="video_goal"
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        video_platform = st.selectbox(
            "Platform",
            ["TikTok", "YouTube", "Instagram Reels", "LinkedIn Video", "Facebook Video", "YouTube Shorts", "Website/Landing Page"],
            key="video_platform"
        )
        
        video_type = st.selectbox(
            "Video Type",
            [
                "🎯 Marketing - Product Demo",
                "🎯 Marketing - Explainer Video",
                "🎯 Marketing - Customer Testimonial",
                "🎯 Marketing - Problem/Solution",
                "🎯 Marketing - Competitor Comparison",
                "🎯 Marketing - Feature Highlight",
                "🎯 Marketing - ROI/Results Showcase",
                "🎯 Marketing - Objection Handler",
                "📚 Educational - How-To Tutorial",
                "📚 Educational - Industry Tips",
                "📚 Educational - USCIS Updates",
                "🎭 Engagement - Day-in-the-Life",
                "🎭 Engagement - Behind-the-Scenes",
                "🎭 Engagement - Team Introduction",
                "🎭 Engagement - FAQ Response",
                "🎭 Engagement - Trending Challenge",
                "📢 Announcement - New Feature",
                "📢 Announcement - Company News",
                "📢 Announcement - Event Promotion"
            ]
        )
        
        video_topic = st.text_input(
            "Video Topic",
            placeholder="e.g., Why immigration firms are switching from spreadsheets to LawTrax",
            key="video_topic"
        )
        
        # Target Persona for Video
        video_persona = st.selectbox(
            "🎯 Target Persona",
            list(TARGET_PERSONAS.keys()),
            key="video_persona"
        )
    
    with col2:
        duration = st.selectbox(
            "Target Duration",
            [
                "15 seconds (TikTok/Reels Hook)",
                "30 seconds (Social Ad)",
                "60 seconds (Explainer)",
                "90 seconds (Product Demo)",
                "2-3 minutes (Deep Dive)",
                "5-7 minutes (Tutorial)",
                "10+ minutes (Comprehensive)"
            ]
        )
        
        video_style = st.selectbox(
            "Style",
            [
                "Talking Head (Founder/Expert)",
                "Screen Recording + Voiceover",
                "Animated Explainer",
                "Customer Interview",
                "Problem/Solution Drama",
                "Side-by-Side Comparison",
                "Text Overlay + B-Roll",
                "Mixed Media",
                "Documentary Style"
            ]
        )
        
        video_cta = st.selectbox(
            "Call-to-Action",
            [
                "Book a Free Demo",
                "Start Your Free Trial",
                "Visit lawtrax.com",
                "Link in Bio",
                "Comment for More Info",
                "Download Our Guide",
                "Call 972-200-1030",
                "See Pricing"
            ],
            key="video_cta"
        )
        
        key_message = st.text_input(
            "Key Message/Hook",
            placeholder="e.g., Stop losing clients to paperwork chaos",
            help="The one thing you want viewers to remember"
        )
    
    # Additional video options
    st.markdown("### 🎥 Video Details")
    vid_detail_col1, vid_detail_col2 = st.columns(2)
    
    with vid_detail_col1:
        pain_points_video = st.multiselect(
            "Pain Points to Address",
            [
                "Manual data entry taking too long",
                "Missing deadlines",
                "Lost documents",
                "No real-time case visibility",
                "Expensive software with hidden fees",
                "Complex, hard-to-use systems",
                "Poor client communication",
                "Compliance concerns",
                "Can't scale with growth",
                "24-hour reporting delays"
            ],
            key="pain_points_video"
        )
        
        proof_points = st.multiselect(
            "Proof Points to Include",
            [
                "30%+ revenue increase",
                "99.9% uptime guarantee",
                "Zero additional API costs",
                "Real-time reporting",
                "25+ years industry experience",
                "Google Cloud security",
                "SOC 2 Type II compliant",
                "Trusted by leading firms"
            ],
            key="proof_points"
        )
    
    with vid_detail_col2:
        competitor_video = st.multiselect(
            "Competitors to Address (Subtle)",
            ["INSZoom", "Docketwise", "LawLogix", "CampLegal", "Spreadsheets/Manual", "Other Legacy Systems"],
            key="competitor_video"
        )
        
        video_context = st.text_area(
            "Additional Requirements",
            placeholder="Specific scenes, testimonial quotes, features to show...",
            height=80,
            key="video_context"
        )
    
    # Generate buttons
    st.markdown("---")
    gen_col1, gen_col2 = st.columns(2)
    
    # Check if video scripts feature is enabled
    video_scripts_enabled = st.session_state.get('enable_video_scripts', False)
    
    with gen_col1:
        generate_script = st.button(
            "📝 Generate Video Script", 
            type="primary", 
            use_container_width=True,
            disabled=not video_scripts_enabled
        )
    
    with gen_col2:
        generate_full_video = st.button(
            "🎬 Generate Full Video Package", 
            type="secondary", 
            use_container_width=True,
            disabled=not video_scripts_enabled
        )
    
    # Show warning if disabled
    if not video_scripts_enabled:
        st.warning("⚠️ **Video Script Generation is DISABLED** to save API tokens. Enable in sidebar → '🎬 Enable Video Scripts'")
    
    if generate_script or generate_full_video:
        if not st.session_state.api_key:
            st.error("⚠️ Please enter your Claude API key in the sidebar")
        elif not video_topic:
            st.error("⚠️ Please enter a video topic")
        else:
            persona_info = TARGET_PERSONAS[video_persona]
            
            if generate_full_video:
                with st.spinner("🎬 Creating comprehensive video marketing package..."):
                    full_video_prompt = f"""You are an expert video marketing strategist and producer specializing in B2B SaaS marketing 
for the legal technology industry, specifically immigration case management software.

COMPANY INFORMATION:
{company_info}

VIDEO MARKETING OBJECTIVE: {video_goal}

TARGET PERSONA: {video_persona}
- Description: {persona_info['description']}
- Pain Points: {', '.join(persona_info['pain_points'])}
- Motivators: {', '.join(persona_info['motivators'])}

PLATFORM: {video_platform}
VIDEO TYPE: {video_type}
TOPIC: {video_topic}
TARGET DURATION: {duration}
STYLE: {video_style}
CALL-TO-ACTION: {video_cta}
KEY MESSAGE/HOOK: {key_message if key_message else 'Create a compelling hook'}

PAIN POINTS TO ADDRESS: {', '.join(pain_points_video) if pain_points_video else 'General industry pain points'}
PROOF POINTS: {', '.join(proof_points) if proof_points else 'Use available metrics'}
COMPETITORS TO SUBTLY ADDRESS: {', '.join(competitor_video) if competitor_video else 'Focus on LawTrax strengths'}

ADDITIONAL CONTEXT: {video_context if video_context else 'None'}

TASK:
Create a COMPREHENSIVE VIDEO MARKETING PACKAGE that includes everything needed to produce and publish this video.

OUTPUT - COMPLETE VIDEO PACKAGE:

## 🎬 VIDEO SCRIPT

### HOOK (First 3 Seconds)
[Attention-grabbing opening that stops the scroll - critical for {video_platform}]

### OPENING (Seconds 4-10)
[Problem statement that resonates with {video_persona}]

### MAIN CONTENT
[Full script with timestamps, speaker directions, and visual cues]
- Include [VISUAL: description] cues for B-roll
- Include [TEXT ON SCREEN: text] for graphics
- Include [TRANSITION: type] for editing

### CALL-TO-ACTION (Final 5-10 seconds)
[Strong CTA: {video_cta}]

---

## 🎨 VISUAL STORYBOARD

| Timestamp | Visual | Audio/Voiceover | Text Overlay |
|-----------|--------|-----------------|--------------|
[Complete scene-by-scene breakdown]

---

## 📱 PLATFORM-SPECIFIC VERSIONS

### {video_platform} Version
- Optimized length and format
- Platform-specific hooks
- Hashtags and description

### Alternative Cuts
- 15-second teaser version
- 30-second ad version
- Full version

---

## 🖼️ THUMBNAIL OPTIONS
[3 thumbnail concepts with descriptions]

---

## ✍️ CAPTIONS & DESCRIPTIONS

### Video Title (SEO Optimized)
[Title]

### Video Description
[Full description with keywords, timestamps, links]

### Hashtags
[Platform-appropriate hashtags]

---

## 🎵 AUDIO RECOMMENDATIONS
- Background music style
- Sound effects
- Voiceover tone and pacing

---

## 📊 POSTING STRATEGY
- Best posting time for {video_platform}
- Engagement strategy
- Cross-posting recommendations
- A/B testing suggestions

---

## 📈 SUCCESS METRICS
- Views target
- Engagement rate goal
- Click-through expectations
- Conversion tracking

---

## 🔄 REPURPOSING IDEAS
- Blog post version
- Social media snippets
- Email content
- Podcast topic

Make this video package comprehensive, professional, and ready for production."""

                    result = get_claude_response(full_video_prompt, st.session_state.api_key)
                    
                    if not result.startswith("ERROR"):
                        st.session_state.generated_content.append({
                            "type": "Full Video Package",
                            "platform": video_platform,
                            "topic": video_topic,
                            "persona": video_persona,
                            "goal": video_goal,
                            "content": result,
                            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")
                        })
                        
                        st.markdown('<div class="success-banner">✅ Complete Video Package Generated!</div>', unsafe_allow_html=True)
                        st.markdown("### 🎬 Your Video Marketing Package")
                        st.markdown(result)
                        
                        st.download_button(
                            label="📥 Download Full Video Package",
                            data=result,
                            file_name=f"video_package_{video_platform.lower()}_{datetime.now().strftime('%Y%m%d_%H%M')}.md",
                            mime="text/markdown"
                        )
                    else:
                        st.error(result)
            
            else:  # generate_script only
                with st.spinner("📝 Creating video script..."):
                    script_prompt = f"""You are an expert video scriptwriter for B2B SaaS marketing in the legal technology space.

COMPANY: LawTrax - Immigration Case Management Software
{company_info}

VIDEO DETAILS:
- Platform: {video_platform}
- Type: {video_type}
- Topic: {video_topic}
- Duration: {duration}
- Style: {video_style}
- Target Persona: {video_persona} - {persona_info['description']}
- CTA: {video_cta}
- Key Message: {key_message if key_message else 'Create compelling hook'}

Pain Points: {', '.join(pain_points_video) if pain_points_video else 'Industry standard'}
Proof Points: {', '.join(proof_points) if proof_points else 'Available metrics'}

Create a complete video script with:

## 🎬 VIDEO SCRIPT

**HOOK (0-3 seconds):**
[Scroll-stopping opening]

**PROBLEM (4-15 seconds):**
[Relate to viewer's pain]

**SOLUTION (Main body):**
[Introduce LawTrax as the answer]
[Include timestamps and visual cues]

**PROOF (Social proof section):**
[Metrics, testimonials, credibility]

**CTA (Final seconds):**
[Clear call-to-action: {video_cta}]

---

## 📋 PRODUCTION NOTES
- B-roll suggestions
- On-screen text
- Music/sound recommendations
- Thumbnail concept

---

## 📝 POST COPY
Caption/description for {video_platform} with hashtags"""

                    result = get_claude_response(script_prompt, st.session_state.api_key)
                    
                    if not result.startswith("ERROR"):
                        st.session_state.generated_content.append({
                            "type": "Video Script",
                            "platform": video_platform,
                            "topic": video_topic,
                            "persona": video_persona,
                            "content": result,
                            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")
                        })
                        
                        st.markdown('<div class="success-banner">✅ Video Script Generated!</div>', unsafe_allow_html=True)
                        st.markdown("### 📝 Your Video Script")
                        st.markdown(result)
                        
                        st.download_button(
                            label="📥 Download Script",
                            data=result,
                            file_name=f"video_script_{video_platform.lower()}_{datetime.now().strftime('%Y%m%d_%H%M')}.md",
                            mime="text/markdown"
                        )
                    else:
                        st.error(result)

# Tab 2b: Generate Videos (AI Video Generation)
with tab2b:
    st.markdown("## 🎥 AI Video Generator")
    st.markdown("Transform your scripts into **actual videos** using AI video generation services")
    
    # Check if feature is enabled
    video_gen_enabled = st.session_state.get('enable_video_generation', False)
    
    if not video_gen_enabled:
        st.warning("⚠️ **Video Generation is DISABLED** to save API tokens. Enable in sidebar → '🎥 Enable Video Generation'")
    
    # Video Generation Method Selection
    st.markdown("### 🎬 Choose Video Generation Method")
    
    video_method = st.selectbox(
        "Select AI Video Platform",
        [
            "🎭 HeyGen - AI Avatar Videos (Best for Talking Head/Presenter)",
            "🎨 Runway Gen-3 - Cinematic AI Videos",
            "⚡ Pika Labs - Fast Stylized Videos", 
            "🎬 Synthesia - Corporate Training Videos",
            "🌟 Luma Dream Machine - Creative Videos",
            "📱 InVideo AI - Social Media Videos",
            "🎯 Manual Export - Get production-ready assets"
        ]
    )
    
    st.markdown("---")
    
    # HeyGen Integration (Best for LawTrax - talking head marketing videos)
    if "HeyGen" in video_method:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 1.5rem; border-radius: 15px; color: white; margin-bottom: 1rem;">
            <h3 style="margin: 0 0 0.5rem 0;">🎭 HeyGen - AI Avatar Videos</h3>
            <p style="margin: 0; opacity: 0.9;">Perfect for LawTrax marketing: Create professional talking-head videos with AI avatars. 
            Ideal for product demos, testimonials, and explainer videos.</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            heygen_api_key = st.text_input(
                "HeyGen API Key (Optional)",
                type="password",
                help="Get your API key from heygen.com/api"
            )
            
            avatar_type = st.selectbox(
                "Avatar Type",
                [
                    "Professional Male (Business)",
                    "Professional Female (Business)", 
                    "Diverse Male Presenter",
                    "Diverse Female Presenter",
                    "Custom Avatar (Upload Your Own)",
                    "Use Stock Avatar"
                ]
            )
            
            video_voice = st.selectbox(
                "Voice Style",
                [
                    "Professional American Male",
                    "Professional American Female",
                    "British Male",
                    "British Female",
                    "Friendly Conversational",
                    "Authoritative Executive"
                ]
            )
        
        with col2:
            heygen_video_length = st.selectbox(
                "Video Length",
                ["30 seconds", "60 seconds", "90 seconds", "2 minutes", "3 minutes", "5 minutes"]
            )
            
            background_style = st.selectbox(
                "Background",
                [
                    "Modern Office",
                    "Law Firm Setting",
                    "Clean White/Minimal",
                    "Tech Gradient",
                    "Custom Background",
                    "Green Screen"
                ]
            )
            
            include_captions = st.checkbox("Include Auto-Captions", value=True)
            include_logo = st.checkbox("Include LawTrax Logo", value=True)
        
        # Script Input
        st.markdown("### 📝 Video Script")
        heygen_script = st.text_area(
            "Enter or paste your video script",
            height=200,
            placeholder="""Hi, I'm here to show you how LawTrax can transform your immigration law practice.

Are you spending hours on paperwork instead of serving clients?

With LawTrax, our clients have seen a 30% increase in revenue by automating case management.

Our platform offers real-time reporting, automated USCIS form generation, and a secure client portal.

Book a free demo today at lawtrax.com.

Let's grow your practice together.""",
            help="Paste your script from the Video Scripts tab or write a new one"
        )
        
        # Generate Video Button
        if st.button("🎬 Generate HeyGen Video", type="primary", use_container_width=True, disabled=not video_gen_enabled):
            if heygen_script:
                # Generate HeyGen-ready package
                with st.spinner("Preparing your video package..."):
                    heygen_prompt = f"""Create a complete HeyGen video production package for this script.

SCRIPT:
{heygen_script}

SETTINGS:
- Avatar: {avatar_type}
- Voice: {video_voice}
- Length: {heygen_video_length}
- Background: {background_style}
- Captions: {include_captions}
- Logo: {include_logo}

OUTPUT:
1. **FORMATTED SCRIPT** (with timing marks and pauses)
2. **SCENE BREAKDOWN** (scene-by-scene with avatar instructions)
3. **HEYGEN SETTINGS** (exact settings to use in HeyGen)
4. **B-ROLL SUGGESTIONS** (scenes to add between talking head)
5. **THUMBNAIL DESCRIPTION** (for YouTube/social)
6. **POST-PRODUCTION TIPS** (how to enhance the final video)

Make it optimized for HeyGen's platform."""

                    result = get_claude_response(heygen_prompt, st.session_state.api_key) if st.session_state.api_key else "Please add your Claude API key to generate the video package."
                    
                    st.markdown('<div class="success-banner">✅ HeyGen Video Package Ready!</div>', unsafe_allow_html=True)
                    
                    # Display results
                    st.markdown("### 📦 Your HeyGen Video Package")
                    st.markdown(result)
                    
                    # Quick Links
                    st.markdown("### 🔗 Quick Actions")
                    link_col1, link_col2, link_col3 = st.columns(3)
                    with link_col1:
                        st.link_button("🎭 Open HeyGen", "https://www.heygen.com/", use_container_width=True)
                    with link_col2:
                        st.link_button("📚 HeyGen Tutorial", "https://www.heygen.com/article/getting-started", use_container_width=True)
                    with link_col3:
                        st.download_button(
                            "📥 Download Package",
                            result if result else heygen_script,
                            file_name=f"heygen_video_package_{datetime.now().strftime('%Y%m%d_%H%M')}.md",
                            mime="text/markdown",
                            use_container_width=True
                        )
            else:
                st.error("Please enter a script")
    
    # Runway Gen-3 Integration
    elif "Runway" in video_method:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #00C9FF 0%, #92FE9D 100%); 
                    padding: 1.5rem; border-radius: 15px; color: #333; margin-bottom: 1rem;">
            <h3 style="margin: 0 0 0.5rem 0;">🎨 Runway Gen-3 Alpha</h3>
            <p style="margin: 0;">Create cinematic AI-generated videos from text prompts. Perfect for B-roll, 
            product visualizations, and creative marketing content.</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            runway_prompt = st.text_area(
                "Video Prompt",
                height=150,
                placeholder="A modern law office with sunlight streaming through windows, showing a lawyer confidently using a tablet, professional atmosphere, cinematic lighting, 4K quality",
                help="Describe the video scene you want to create"
            )
            
            runway_duration = st.selectbox(
                "Duration",
                ["4 seconds", "8 seconds", "12 seconds", "16 seconds"]
            )
        
        with col2:
            runway_style = st.selectbox(
                "Style",
                [
                    "Cinematic / Film",
                    "Corporate / Professional",
                    "Modern / Tech",
                    "Documentary",
                    "Commercial / Ad",
                    "Abstract / Artistic"
                ]
            )
            
            runway_motion = st.select_slider(
                "Camera Motion",
                options=["Static", "Subtle", "Moderate", "Dynamic", "Dramatic"]
            )
        
        if st.button("🎨 Generate Runway Prompt Package", type="primary", use_container_width=True, disabled=not video_gen_enabled):
            with st.spinner("Creating optimized Runway prompts..."):
                runway_gen_prompt = f"""Create an optimized Runway Gen-3 video generation package.

USER REQUEST:
- Scene: {runway_prompt}
- Duration: {runway_duration}
- Style: {runway_style}
- Motion: {runway_motion}

COMPANY CONTEXT: LawTrax Immigration Software Marketing

OUTPUT:
1. **OPTIMIZED PROMPT** (Runway-formatted, detailed prompt)
2. **NEGATIVE PROMPT** (what to avoid)
3. **CAMERA SETTINGS** (movement, angle recommendations)
4. **3 ALTERNATIVE PROMPTS** (variations for A/B testing)
5. **SCENE SEQUENCE** (if creating multiple clips for editing)
6. **POST-PRODUCTION** (how to use these clips in final video)
7. **SOUNDTRACK SUGGESTIONS** (royalty-free music style)

Make prompts specific, detailed, and optimized for Runway Gen-3's capabilities."""

                result = get_claude_response(runway_gen_prompt, st.session_state.api_key) if st.session_state.api_key else "Please add your Claude API key."
                
                st.markdown('<div class="success-banner">✅ Runway Package Ready!</div>', unsafe_allow_html=True)
                st.markdown(result)
                
                st.markdown("### 🔗 Quick Actions")
                link_col1, link_col2 = st.columns(2)
                with link_col1:
                    st.link_button("🎨 Open Runway", "https://app.runwayml.com/", use_container_width=True)
                with link_col2:
                    st.download_button(
                        "📥 Download Prompts",
                        result if result else runway_prompt,
                        file_name=f"runway_prompts_{datetime.now().strftime('%Y%m%d_%H%M')}.md",
                        mime="text/markdown",
                        use_container_width=True
                    )
    
    # Pika Labs Integration
    elif "Pika" in video_method:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #FF6B6B 0%, #FFE66D 100%); 
                    padding: 1.5rem; border-radius: 15px; color: #333; margin-bottom: 1rem;">
            <h3 style="margin: 0 0 0.5rem 0;">⚡ Pika Labs</h3>
            <p style="margin: 0;">Fast, stylized AI video generation. Great for social media content, 
            quick iterations, and creative experimentation.</p>
        </div>
        """, unsafe_allow_html=True)
        
        pika_prompt = st.text_area(
            "Pika Video Prompt",
            height=150,
            placeholder="Immigration attorney reviewing documents on tablet, modern office, warm lighting, professional"
        )
        
        col1, col2, col3 = st.columns(3)
        with col1:
            pika_aspect = st.selectbox("Aspect Ratio", ["16:9", "9:16", "1:1", "4:5"])
        with col2:
            pika_motion = st.slider("Motion Level", 1, 5, 3)
        with col3:
            pika_guidance = st.slider("Prompt Guidance", 1, 20, 12)
        
        if st.button("⚡ Generate Pika Package", type="primary", use_container_width=True, disabled=not video_gen_enabled):
            with st.spinner("Creating Pika prompts..."):
                pika_gen_prompt = f"""Create an optimized Pika Labs video generation package.

PROMPT: {pika_prompt}
SETTINGS: Aspect {pika_aspect}, Motion {pika_motion}, Guidance {pika_guidance}
CONTEXT: LawTrax Immigration Software Marketing

OUTPUT:
1. **OPTIMIZED PIKA PROMPT** (formatted for Pika's style)
2. **PARAMETERS** (exact /create command)
3. **PIKAFFECTS** (effects to apply post-generation)
4. **3 VARIATIONS** (for testing)
5. **BEST USE CASES** (where to use this video)"""

                result = get_claude_response(pika_gen_prompt, st.session_state.api_key) if st.session_state.api_key else "Please add your Claude API key."
                
                st.markdown('<div class="success-banner">✅ Pika Package Ready!</div>', unsafe_allow_html=True)
                st.markdown(result)
                
                st.link_button("⚡ Open Pika Labs", "https://pika.art/", use_container_width=True)
    
    # Synthesia Integration
    elif "Synthesia" in video_method:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #4B0082 0%, #9370DB 100%); 
                    padding: 1.5rem; border-radius: 15px; color: white; margin-bottom: 1rem;">
            <h3 style="margin: 0 0 0.5rem 0;">🎬 Synthesia</h3>
            <p style="margin: 0;">Enterprise-grade AI video platform. Perfect for training videos, 
            corporate communications, and professional presentations.</p>
        </div>
        """, unsafe_allow_html=True)
        
        synthesia_script = st.text_area(
            "Synthesia Script",
            height=200,
            placeholder="Enter your professional script here..."
        )
        
        col1, col2 = st.columns(2)
        with col1:
            synthesia_avatar = st.selectbox("Avatar", ["Professional Male", "Professional Female", "Diverse Options"])
            synthesia_lang = st.selectbox("Language", ["English (US)", "English (UK)", "Spanish", "French", "German"])
        with col2:
            synthesia_template = st.selectbox("Template", ["Corporate", "Training", "Marketing", "Minimal"])
            synthesia_brand = st.checkbox("Include LawTrax Branding", value=True)
        
        if st.button("🎬 Generate Synthesia Package", type="primary", use_container_width=True, disabled=not video_gen_enabled):
            st.markdown('<div class="success-banner">✅ Ready for Synthesia!</div>', unsafe_allow_html=True)
            st.markdown(f"""
### Your Synthesia Setup

**Script:** Ready to paste
**Avatar:** {synthesia_avatar}
**Language:** {synthesia_lang}
**Template:** {synthesia_template}

### Next Steps:
1. Go to [Synthesia](https://www.synthesia.io/)
2. Create new video
3. Select avatar: {synthesia_avatar}
4. Paste your script
5. Add branding elements
6. Generate and download
            """)
            st.link_button("🎬 Open Synthesia", "https://www.synthesia.io/", use_container_width=True)
    
    # Manual Export Option
    elif "Manual" in video_method:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #2C3E50 0%, #3498DB 100%); 
                    padding: 1.5rem; border-radius: 15px; color: white; margin-bottom: 1rem;">
            <h3 style="margin: 0 0 0.5rem 0;">🎯 Production-Ready Export</h3>
            <p style="margin: 0;">Get all assets needed to produce your video with any tool or 
            send to a video production team.</p>
        </div>
        """, unsafe_allow_html=True)
        
        export_script = st.text_area(
            "Your Video Script",
            height=200,
            placeholder="Paste your script here to generate a complete production package..."
        )
        
        export_format = st.selectbox(
            "Export Format",
            [
                "Complete Production Brief (PDF-ready)",
                "Storyboard Document",
                "Shot List + Script",
                "Social Media Package (All Platforms)",
                "Agency Brief"
            ]
        )
        
        if st.button("📦 Generate Production Package", type="primary", use_container_width=True, disabled=not video_gen_enabled):
            if export_script:
                with st.spinner("Creating production package..."):
                    export_prompt = f"""Create a complete video production package for this script.

SCRIPT:
{export_script}

FORMAT: {export_format}
BRAND: LawTrax Immigration Software

OUTPUT:
1. **PRODUCTION BRIEF** (overview, objectives, target audience)
2. **COMPLETE STORYBOARD** (scene-by-scene with descriptions)
3. **SHOT LIST** (numbered shots with framing, duration, notes)
4. **VISUAL REFERENCES** (describe reference images/videos)
5. **AUDIO GUIDE** (music style, voiceover notes, sound effects)
6. **BRANDING GUIDELINES** (colors, logo placement, fonts)
7. **TECHNICAL SPECS** (resolution, format, duration)
8. **PLATFORM VERSIONS** (cuts for different social platforms)
9. **TALENT NOTES** (if using actors/presenters)
10. **TIMELINE** (production schedule estimate)

Make this comprehensive enough to hand to any video production team or freelancer."""

                    result = get_claude_response(export_prompt, st.session_state.api_key) if st.session_state.api_key else "Please add your Claude API key."
                    
                    st.markdown('<div class="success-banner">✅ Production Package Complete!</div>', unsafe_allow_html=True)
                    st.markdown(result)
                    
                    st.download_button(
                        "📥 Download Production Package",
                        result,
                        file_name=f"video_production_package_{datetime.now().strftime('%Y%m%d_%H%M')}.md",
                        mime="text/markdown",
                        use_container_width=True
                    )
            else:
                st.error("Please enter a script")
    
    # Other platforms - show quick links
    else:
        st.markdown("### 🔗 Quick Access to Video Platforms")
        
        platform_col1, platform_col2, platform_col3 = st.columns(3)
        
        with platform_col1:
            st.link_button("🎭 HeyGen", "https://www.heygen.com/", use_container_width=True)
            st.link_button("🎨 Runway", "https://app.runwayml.com/", use_container_width=True)
        
        with platform_col2:
            st.link_button("⚡ Pika Labs", "https://pika.art/", use_container_width=True)
            st.link_button("🎬 Synthesia", "https://www.synthesia.io/", use_container_width=True)
        
        with platform_col3:
            st.link_button("🌟 Luma AI", "https://lumalabs.ai/", use_container_width=True)
            st.link_button("📱 InVideo", "https://invideo.io/", use_container_width=True)
    
    # Tips Section
    st.markdown("---")
    st.markdown("### 💡 AI Video Generation Tips for LawTrax Marketing")
    
    tips_col1, tips_col2 = st.columns(2)
    
    with tips_col1:
        st.markdown("""
        **Best Platforms by Use Case:**
        
        🎭 **HeyGen** - Talking head videos, demos, testimonials
        - Best for: Product explainers, founder messages
        - Cost: ~$2.40 per 10-second video
        
        🎨 **Runway** - Cinematic B-roll, visualizations
        - Best for: Background footage, transitions
        - Cost: ~$0.50 per 5-second clip
        
        ⚡ **Pika** - Quick social content
        - Best for: TikTok, Reels, fast iterations
        - Cost: Free tier available
        """)
    
    with tips_col2:
        st.markdown("""
        **LawTrax Video Ideas:**
        
        📹 **Product Demo** (HeyGen + Screen Recording)
        - AI avatar introduces, screen shows platform
        
        🎬 **Client Testimonial** (HeyGen)
        - Professional avatar shares success story
        
        🎥 **Explainer Video** (Synthesia)
        - How LawTrax solves immigration firm pain points
        
        📱 **Social Clips** (Pika/Runway)
        - Quick tips, stats, feature highlights
        """)

# Tab 3: SEO Content
with tab3:
    st.markdown("## 🔍 SEO Content Generator")
    st.markdown(f"Creating SEO-optimized marketing content for **{company_display_name}**")
    
    # SEO Goal
    st.markdown("### 🎯 SEO Content Goal")
    seo_goal = st.selectbox(
        "Content Objective",
        [
            "Rank for Product Keywords (Bottom Funnel)",
            "Rank for Problem Keywords (Middle Funnel)",
            "Build Topical Authority (Top Funnel)",
            "Capture Competitor Keywords",
            "Target Long-Tail Questions",
            "Create Linkable Asset"
        ],
        key="seo_goal"
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        seo_content_type = st.selectbox(
            "Content Type",
            [
                "Blog Post - How To Guide",
                "Blog Post - Listicle",
                "Blog Post - Comparison (vs Competitors)",
                "Blog Post - Ultimate Guide",
                "Landing Page - Product",
                "Landing Page - Use Case",
                "Landing Page - Industry",
                "Pillar Page - Comprehensive",
                "Case Study",
                "FAQ Page",
                "Glossary/Definition Page"
            ],
            key="seo_content_type"
        )
        
        primary_keyword = st.text_input(
            "Primary Keyword",
            placeholder="e.g., immigration case management software",
            help="Main keyword to target"
        )
        
        secondary_keywords = st.text_area(
            "Secondary Keywords",
            placeholder="immigration software for law firms\nUSCIS case tracking\nimmigration attorney software\nbest immigration case management",
            help="Additional keywords (one per line)",
            height=100
        )
        
        # Persona for SEO
        seo_persona = st.selectbox(
            "🎯 Target Persona",
            list(TARGET_PERSONAS.keys()),
            key="seo_persona"
        )
    
    with col2:
        target_word_count = st.select_slider(
            "Target Word Count",
            options=[500, 750, 1000, 1500, 2000, 2500, 3000, 4000, 5000],
            value=2000
        )
        
        search_intent = st.selectbox(
            "Search Intent",
            [
                "Informational (How to, What is, Guide)",
                "Commercial (Best, Top, Compare, Review)",
                "Transactional (Buy, Pricing, Demo, Trial)",
                "Navigational (Brand-specific)"
            ]
        )
        
        competitor_keywords = st.multiselect(
            "Competitor Keywords to Target",
            [
                "INSZoom alternative",
                "Docketwise vs",
                "LawLogix competitor",
                "CampLegal alternative",
                "best immigration software",
                "immigration case management comparison"
            ],
            key="competitor_keywords"
        )
        
        seo_context = st.text_area(
            "Additional Requirements",
            placeholder="Specific angle, target audience details, internal links to include...",
            height=80,
            key="seo_context"
        )
    
    # SEO Tips
    persona_seo = TARGET_PERSONAS[seo_persona]
    st.markdown(f"""
    <div class="info-box">
        <strong>📌 SEO Best Practices for {seo_persona}:</strong><br>
        • Content Focus: {persona_seo['content_focus']}<br>
        • Pain Points to Address: {', '.join(persona_seo['pain_points'][:3])}<br>
        • Tone: {persona_seo['tone']}
    </div>
    """, unsafe_allow_html=True)
    
    # Check if SEO is enabled
    seo_enabled = st.session_state.get('enable_seo_content', True)
    
    if not seo_enabled:
        st.warning("⚠️ **SEO Content Generation is DISABLED**. Enable in sidebar → '🔍 Enable SEO Content'")
    
    if st.button("🔍 Generate SEO Content", type="primary", use_container_width=True, disabled=not seo_enabled):
        if not st.session_state.api_key:
            st.error("⚠️ Please enter your Claude API key in the sidebar")
        elif not primary_keyword:
            st.error("⚠️ Please enter a primary keyword")
        else:
            with st.spinner("📝 Creating SEO-optimized marketing content..."):
                seo_prompt = f"""You are an expert SEO content strategist specializing in B2B SaaS marketing for legal technology, 
specifically immigration case management software. You understand search intent, keyword optimization, and conversion-focused content.

COMPANY INFORMATION:
{company_info}

SEO CONTENT GOAL: {seo_goal}
CONTENT TYPE: {seo_content_type}
PRIMARY KEYWORD: {primary_keyword}
SECONDARY KEYWORDS: {secondary_keywords}
TARGET WORD COUNT: {target_word_count}
SEARCH INTENT: {search_intent}

TARGET PERSONA: {seo_persona}
- Description: {persona_seo['description']}
- Pain Points: {', '.join(persona_seo['pain_points'])}
- Motivators: {', '.join(persona_seo['motivators'])}
- Content Focus: {persona_seo['content_focus']}

COMPETITOR KEYWORDS TO TARGET: {', '.join(competitor_keywords) if competitor_keywords else 'Focus on primary keyword'}

ADDITIONAL CONTEXT: {seo_context if seo_context else 'None'}

TASK:
Create comprehensive SEO-optimized content that:
1. Ranks for "{primary_keyword}" and related terms
2. Speaks directly to {seo_persona}'s needs and pain points
3. Positions LawTrax as the ideal solution
4. Includes natural calls-to-action throughout
5. Is structured for featured snippets where applicable
6. Builds topical authority in immigration law technology

OUTPUT FORMAT:

## 📊 SEO METADATA

**Meta Title (50-60 chars):**
[Title optimized for CTR and keywords]

**Meta Description (150-160 chars):**
[Compelling description with keyword and CTA]

**URL Slug:**
[SEO-friendly URL]

**Target Featured Snippet:**
[Optimized answer for position zero]

---

## 📝 FULL CONTENT

[Complete {target_word_count}-word article with:]
- H1, H2, H3 heading structure
- Primary keyword in first 100 words
- Secondary keywords naturally distributed
- Internal linking opportunities marked as [INTERNAL LINK: anchor text -> page]
- External linking opportunities marked as [EXTERNAL LINK: anchor text]
- Image alt text suggestions marked as [IMAGE: description, alt text]
- CTAs integrated naturally throughout

---

## 📈 SEO ANALYSIS

**Keyword Usage:**
- Primary keyword density
- Secondary keyword coverage
- LSI keywords included

**On-Page Optimization:**
- Heading structure analysis
- Internal linking suggestions
- Schema markup recommendations

**Content Enhancement:**
- FAQ section for additional keywords
- Table of contents
- Key takeaways box

---

## 🎯 CONVERSION OPTIMIZATION

**CTA Placements:**
[Strategic CTA locations and copy]

**Lead Magnets:**
[Related downloadable content ideas]

**Next Steps:**
[Reader journey recommendations]

Make the content authoritative, comprehensive, and designed to rank AND convert for LawTrax."""

                result = get_claude_response(seo_prompt, st.session_state.api_key)
                
                if not result.startswith("ERROR"):
                    st.session_state.generated_content.append({
                        "type": "SEO Content",
                        "platform": "Website/Blog",
                        "topic": primary_keyword,
                        "persona": seo_persona,
                        "goal": seo_goal,
                        "content": result,
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")
                    })
                    
                    st.markdown('<div class="success-banner">✅ SEO Content Generated!</div>', unsafe_allow_html=True)
                    st.markdown("### 📝 Generated SEO Content")
                    st.markdown(result)
                    
                    st.download_button(
                        label="📥 Download Content",
                        data=result,
                        file_name=f"seo_{seo_content_type.lower().replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M')}.md",
                        mime="text/markdown"
                    )
                else:
                    st.error(result)

# Tab 4: Knowledge Base
with tab4:
    st.markdown("## 📚 Company Knowledge Base")
    
    if use_default:
        st.markdown("### LawTrax - Immigration Case Management Software")
        
        # Key Features Section
        st.markdown("#### 🎯 Key Features")
        features = [
            ("Case Management", "Workflow-based platform with multiple stages based on case type"),
            ("Customer Management", "Secure cloud portal for companies and beneficiaries"),
            ("Lead Management", "Built-in CRM for converting prospects to customers"),
            ("Document Management", "Cloud-based, indexable, searchable document system"),
            ("Dashboard Reporting", "Real-time business-driven dashboards with drill-down"),
            ("PDF Generation", "Auto-generates USCIS/DoL formatted documents"),
            ("Client Portal", "Secure uploads and case tracking with notifications"),
            ("Integrations", "Outlook, QuickBooks, webhooks, and RESTful APIs")
        ]
        
        cols = st.columns(2)
        for i, (feature, desc) in enumerate(features):
            with cols[i % 2]:
                st.markdown(f"""
                <div class="feature-card">
                    <strong>{feature}</strong><br>
                    <small>{desc}</small>
                </div>
                """, unsafe_allow_html=True)
                st.markdown("")
        
        # Competitive Advantages
        st.markdown("#### 💪 Competitive Advantages")
        advantages = [
            "✅ No additional API costs (unlike competitors)",
            "✅ True real-time reporting (no 24-hour batch delays)",
            "✅ 99.9% uptime on Google Cloud infrastructure",
            "✅ Built-in USCIS/DoL PDF generator",
            "✅ Complete audit trail for compliance",
            "✅ 30%+ revenue increase reported by clients"
        ]
        for adv in advantages:
            st.markdown(adv)
        
        # Target Market
        st.markdown("#### 🎯 Target Market")
        targets = ["Immigration law firms (solo to enterprise)", "Corporate immigration departments", 
                   "Global mobility teams", "Legal service providers"]
        st.markdown(" | ".join(targets))
        
        # Content Inspiration
        st.markdown("#### 💡 Content Topic Ideas")
        topics = {
            "Educational": [
                "How to streamline H-1B processing with case management software",
                "5 signs your law firm needs to upgrade immigration software",
                "The complete guide to USCIS form automation",
                "Why real-time reporting matters for immigration law firms"
            ],
            "Thought Leadership": [
                "The future of immigration law technology",
                "How AI is transforming immigration case management",
                "Cloud security best practices for law firms",
                "Building a scalable immigration practice"
            ],
            "Client Success": [
                "How [Client] increased revenue 30% with LawTrax",
                "Case study: Reducing administrative burden in immigration law",
                "From manual to automated: A law firm's digital transformation"
            ],
            "Product": [
                "Introducing our new client portal features",
                "How our document management saves 10+ hours weekly",
                "Behind the scenes: How we ensure 99.9% uptime"
            ]
        }
        
        for category, ideas in topics.items():
            with st.expander(f"📌 {category} Topics"):
                for idea in ideas:
                    st.markdown(f"• {idea}")
    else:
        if st.session_state.company_profile:
            profile = st.session_state.company_profile
            st.markdown(f"### {profile.get('name', 'Your Company')}")
            st.markdown(f"**Website:** {profile.get('website', 'Not specified')}")
            st.markdown(f"**Target Market:** {profile.get('target_market', 'Not specified')}")
            st.markdown("#### Description")
            st.markdown(profile.get('description', 'No description provided'))
            st.markdown("#### Key Features")
            st.markdown(profile.get('features', 'No features listed'))
        else:
            st.warning("⚠️ Please configure your company profile in the sidebar")

# Tab 5: Content History
with tab5:
    st.markdown("## 📋 Content History")
    
    if st.session_state.generated_content:
        for i, item in enumerate(reversed(st.session_state.generated_content)):
            with st.expander(f"📄 {item['type']} - {item['platform']} - {item['topic'][:50]}... ({item['timestamp']})"):
                st.markdown(item['content'])
                col1, col2 = st.columns([1, 4])
                with col1:
                    st.download_button(
                        label="📥 Download",
                        data=item['content'],
                        file_name=f"content_{i}_{datetime.now().strftime('%Y%m%d')}.txt",
                        mime="text/plain",
                        key=f"download_{i}"
                    )
    else:
        st.info("📭 No content generated yet. Start creating content in the other tabs!")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    <p>Marketing Command Center | Powered by Claude AI</p>
    <p><small>Configure your API key in the sidebar to start generating content</small></p>
</div>
""", unsafe_allow_html=True)
