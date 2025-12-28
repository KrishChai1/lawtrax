# 🚀 Marketing Command Center

## AI-Powered Content Generation Platform for Immigration Software Marketing

A comprehensive Streamlit application for SEO, social media content generation, video scripting, and lead generation marketing. Built with Claude AI integration.

![Platform Preview](https://img.shields.io/badge/Powered%20by-Claude%20AI-purple)
![Streamlit](https://img.shields.io/badge/Built%20with-Streamlit-red)
![Python](https://img.shields.io/badge/Python-3.8+-blue)

---

## ✨ Features

### 📱 Social Media Content Generator
Generate platform-optimized content for:
- **LinkedIn** - Professional thought leadership posts
- **Instagram** - Engaging visual content with carousels
- **TikTok** - Short-form video captions and hooks
- **YouTube** - Video descriptions and titles
- **Twitter/X** - Threads and tweets
- **Facebook** - Community-focused posts

Each platform includes:
- Character limit optimization
- Hashtag recommendations
- Best posting times
- Format suggestions
- Tone customization

### 🎬 Video Script Generator
Create complete video scripts including:
- Hook and opening (first 3 seconds)
- Main content with timestamps
- B-roll suggestions
- On-screen text recommendations
- Thumbnail concepts
- Captions and hashtags

Supports multiple formats:
- Product demos
- Educational/How-To
- Testimonials/Case studies
- Industry tips
- Behind-the-scenes
- FAQ/Q&A sessions

### 🔍 SEO Content Generator
Produce search-optimized content:
- Blog posts
- Landing pages
- Product/Service pages
- Comparison articles
- How-To guides
- Listicles
- Case studies

Includes:
- Meta titles and descriptions
- Heading structure (H1, H2, H3)
- Keyword density analysis
- Internal linking suggestions
- Featured snippet optimization
- FAQ sections for additional keywords

### 📚 Knowledge Base
Pre-loaded with comprehensive LawTrax information:
- Company features and benefits
- Competitive advantages
- Target market details
- Content topic inspiration
- Success metrics

### 🔄 Flexible Company Support
- **Default Mode**: Pre-configured for LawTrax
- **Custom Mode**: Enter any company's information to generate branded content

---

## 🚀 Quick Start

### 1. Clone or Download
```bash
# Clone the repository
git clone <your-repo-url>
cd lawtrax-marketing-platform
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Get Your Claude API Key
1. Visit [console.anthropic.com](https://console.anthropic.com)
2. Create an account or sign in
3. Navigate to API Keys
4. Create a new API key
5. Copy the key (starts with `sk-ant-...`)

### 4. Run the Application
```bash
streamlit run lawtrax_marketing_platform.py
```

### 5. Configure the App
1. Open the app in your browser (usually http://localhost:8501)
2. Enter your Claude API key in the sidebar
3. Choose to use LawTrax or configure your own company
4. Start generating content!

---

## 📖 Usage Guide

### Generating Social Media Content

1. **Select Platform**: Choose from LinkedIn, Instagram, TikTok, etc.
2. **Choose Content Type**: Educational, Success Story, Product Feature, etc.
3. **Enter Topic**: Describe what the post should be about
4. **Set Target Audience**: Who should this content reach?
5. **Select Tone**: Professional, Conversational, Educational, etc.
6. **Add Context** (Optional): Any specific requirements
7. **Generate**: Click the button and wait for AI-generated content

### Creating Video Scripts

1. **Select Platform**: TikTok, YouTube, Instagram Reels, etc.
2. **Choose Video Type**: Demo, Tutorial, Testimonial, etc.
3. **Enter Topic**: What the video should cover
4. **Set Duration**: From 15 seconds to 10+ minutes
5. **Select Style**: Talking head, Screen recording, Animation, etc.
6. **Generate**: Get a complete script with B-roll suggestions

### Producing SEO Content

1. **Select Content Type**: Blog, Landing Page, Guide, etc.
2. **Enter Primary Keyword**: Main search term to target
3. **Add Secondary Keywords**: Supporting terms (optional)
4. **Set Word Count**: From 500 to 5000 words
5. **Choose Search Intent**: Informational, Commercial, etc.
6. **Generate**: Receive fully optimized content with meta tags

---

## 🏗️ Project Structure

```
lawtrax-marketing-platform/
├── lawtrax_marketing_platform.py   # Main Streamlit application
├── requirements.txt                 # Python dependencies
└── README.md                       # This file
```

---

## 🔧 Configuration Options

### Environment Variables (Optional)
You can set your API key as an environment variable:
```bash
export ANTHROPIC_API_KEY="your-api-key-here"
```

### Streamlit Deployment
For deployment to Streamlit Cloud:
1. Push code to GitHub
2. Connect repo to [share.streamlit.io](https://share.streamlit.io)
3. Add API key in Streamlit secrets management

---

## 💡 Content Ideas Pre-loaded

### Educational Topics
- How to streamline H-1B processing
- 5 signs you need to upgrade immigration software
- Complete guide to USCIS form automation
- Why real-time reporting matters

### Thought Leadership
- The future of immigration law technology
- How AI is transforming case management
- Cloud security best practices
- Building a scalable immigration practice

### Product Marketing
- Feature spotlights and demos
- Client success stories
- Behind-the-scenes content
- Comparison content

---

## 🔒 Security Notes

- API keys are stored only in session state (not persisted)
- No content is stored on external servers
- All processing happens through secure Claude API calls
- Company information stays local to your session

---

## 🛠️ Customization

### Adding New Platforms
Edit the `PLATFORM_GUIDELINES` dictionary to add new social platforms:

```python
PLATFORM_GUIDELINES["NewPlatform"] = {
    "max_chars": 1000,
    "hashtags": 5,
    "tone": "Professional",
    "format": "Posts",
    "best_practices": ["Tip 1", "Tip 2"],
    "content_types": ["Type 1", "Type 2"]
}
```

### Modifying Company Knowledge
Update the `LAWTRAX_KNOWLEDGE` string with your company's information, or use the custom company mode in the sidebar.

---

## 📊 Best Practices

1. **Be Specific**: More detailed prompts generate better content
2. **Use Context**: Add relevant background information
3. **Review Output**: Always review and customize AI-generated content
4. **Test Variations**: Generate multiple versions and A/B test
5. **Track Performance**: Monitor which content types perform best

---

## 🤝 Support

For questions about:
- **LawTrax Product**: info@lawtrax.com | 972-200-1030
- **This Application**: Create an issue in the repository
- **Claude API**: [Anthropic Support](https://support.anthropic.com)

---

## 📄 License

This application is provided for marketing and content generation purposes. Please ensure compliance with your organization's content policies and AI usage guidelines.

---

## 🚀 Roadmap

Future enhancements planned:
- [ ] Content calendar integration
- [ ] Analytics dashboard
- [ ] Competitor content analysis
- [ ] Brand voice training
- [ ] Multi-language support
- [ ] Image generation integration
- [ ] Automated posting capabilities

---

Built with ❤️ for immigration law marketing teams
