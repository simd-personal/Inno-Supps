# Inno Supps PromptOps Playbook

This playbook demonstrates the expected daily workflow for using the PromptOps MVP.

## 🎯 Daily Workflow

### 1. Create an Offer
**Goal**: Generate a compelling offer for a fat loss product

1. Navigate to **Offer Creator** module
2. Fill out the form:
   - **Audience**: "busy professionals aged 30-50 struggling with belly fat"
   - **Pain**: "tried every diet but can't lose stubborn belly fat"
   - **Solution**: "fat loss supplement with clinically-proven ingredients"
   - **Proof**: "clinical study shows 12% more fat loss, 10,000+ customers, 30-day guarantee"
   - **Price**: "$97 with 50% discount for first-time buyers"
   - **Guarantee**: "30-day money-back guarantee"
3. Click **Create Offer**
4. Review the generated JSON output
5. Copy or save the generation

**Expected Output**:
```json
{
  "promise": "Finally Lose Stubborn Belly Fat in 30 Days - Guaranteed",
  "proof_pillars": [
    "Clinical study shows 12% more fat loss",
    "10,000+ customers lost 15+ lbs",
    "30-day money-back guarantee"
  ],
  "price": "$97 (50% off - Limited Time)",
  "guarantee": "30-day money-back guarantee",
  "cta": "Start Your Transformation Today",
  "landing_blurb": "Join thousands who've finally lost stubborn belly fat with our clinically-proven formula. 30-day guarantee."
}
```

### 2. Generate Cold Email
**Goal**: Create a high-converting cold email campaign

1. Navigate to **Cold Email Writer** module
2. Fill out the form:
   - **Audience**: "fitness enthusiasts hitting muscle plateaus"
   - **Pain**: "working out hard but not seeing muscle gains"
   - **Proof**: "proven formula used by 5,000+ athletes"
   - **CTA**: "schedule a free consultation"
3. Click **Generate Cold Email**
4. Review compliance notes
5. Copy the email content

**Expected Output**:
```json
{
  "subject": "Break Through Your Muscle Plateau",
  "body": "Hi [Name], I noticed you're serious about fitness but hitting a plateau. Our clients typically see 20% more gains in 8 weeks. Want to learn how?",
  "tone": "professional but friendly",
  "compliance_notes": "Avoid specific claims about muscle growth percentages"
}
```

### 3. Generate Ad Variants
**Goal**: Create three ad variants for Meta Facebook

1. Navigate to **Ad Writer** module
2. Fill out the form:
   - **Channel**: "Meta Facebook"
   - **Audience**: "men 25-45 interested in fitness and supplements"
   - **Pain/Benefit**: "muscle building and strength gains"
3. Click **Generate Ad Variants**
4. Review all three variants
5. Select the best performing angle

**Expected Output**: Three variants with different psychological angles:
- **Proof-Based**: Focus on clinical studies and data
- **Transformation**: Focus on before/after results
- **Social Proof**: Focus on customer testimonials

### 4. Build n8n Workflow
**Goal**: Automate lead processing workflow

1. Navigate to **Workflow Builder** module
2. Describe the workflow:
   - "When a new lead fills out the fat loss supplement form, send them a welcome email, add them to the CRM, and notify the sales team in Slack"
3. Click **Build Workflow**
4. Review the generated n8n JSON
5. Click **Import to n8n**

**Expected Output**: n8n workflow with:
- Webhook trigger for form submission
- Email node for welcome message
- CRM integration node
- Slack notification node

### 5. Check Slack Summary
**Goal**: Review daily performance and alerts

1. Open Slack workspace
2. Type `/inno summary today`
3. Review the daily digest:
   - Top performing campaigns by adjusted ROAS
   - Recent generations
   - High-risk compliance flags

**Expected Output**:
```
📊 Daily Inno Supps Summary

🏆 Top Performing Campaigns (by Adjusted ROAS)
1. Fat Loss Pro - ROAS: 4.2x, Margin: 60%, Adj ROAS: 2.52x
2. Muscle Builder - ROAS: 3.8x, Margin: 55%, Adj ROAS: 2.09x
3. Energy Boost - ROAS: 5.1x, Margin: 70%, Adj ROAS: 3.57x

📝 Recent Generations
• offer_creator_v1 - 14:30 - Status: completed
• cold_email_v1 - 10:15 - Status: completed
• ad_writer_v1 - 09:45 - Status: completed

⚠️ High Risk Compliance Flags
• Risk Score: 0.85 - generation - 3 issues
```

## 🔄 Weekly Workflow

### Monday: Content Planning
- Review previous week's performance
- Plan content themes for the week
- Generate 5-10 offers for different products
- Create email sequences for each offer

### Tuesday: Ad Campaign Setup
- Generate ad variants for all offers
- Set up A/B tests
- Configure targeting based on suggestions
- Launch campaigns

### Wednesday: Workflow Optimization
- Review n8n workflows
- Optimize based on performance data
- Create new automation workflows
- Test workflow integrations

### Thursday: Compliance Review
- Review all compliance flags
- Update approved language database
- Fix high-risk content
- Train team on compliance guidelines

### Friday: Performance Analysis
- Analyze campaign performance
- Review generation quality scores
- Identify optimization opportunities
- Plan next week's improvements

## 📊 Key Metrics to Track

### Content Performance
- **Generation Success Rate**: % of successful generations
- **Compliance Risk Score**: Average risk across all content
- **Quality Score**: Average rubric scores (clarity, specificity, etc.)

### Campaign Performance
- **ROAS**: Return on ad spend
- **Adjusted ROAS**: ROAS × profit margin
- **Email Open Rates**: Cold email performance
- **Conversion Rates**: Offer to purchase

### Workflow Efficiency
- **Automation Coverage**: % of processes automated
- **Workflow Success Rate**: % of workflows running without errors
- **Time Saved**: Hours saved through automation

## 🚨 Troubleshooting

### Common Issues

**Generation Fails**
- Check OpenAI API key
- Verify input format
- Review error logs: `make logs-api`

**n8n Import Fails**
- Check n8n container status
- Verify webhook configuration
- Test n8n connectivity

**Compliance Alerts**
- Review flagged content
- Update approved language
- Use suggested rewrites

**Slack Bot Not Responding**
- Check bot token configuration
- Verify Slack app permissions
- Test webhook connectivity

### Debug Commands

```bash
# Check all services
docker-compose ps

# View API logs
make logs-api

# Test API health
curl http://localhost:8000/health

# Run demo script
make demo

# Check database
docker-compose exec postgres psql -U postgres -d inno_supps
```

## 🎯 Success Indicators

### Daily Success
- ✅ All five modules accessible and functional
- ✅ Generated content passes compliance checks
- ✅ n8n workflows import successfully
- ✅ Slack bot responds to commands
- ✅ No critical errors in logs

### Weekly Success
- ✅ 50+ content generations
- ✅ <5% high-risk compliance flags
- ✅ 3+ new n8n workflows created
- ✅ 10+ Slack summaries generated
- ✅ All integrations working smoothly

### Monthly Success
- ✅ 200+ content generations
- ✅ <2% high-risk compliance flags
- ✅ 15+ n8n workflows in production
- ✅ Measurable time savings from automation
- ✅ Team adoption of all modules

## 🔧 Maintenance

### Daily
- Monitor service health
- Check error logs
- Review compliance flags
- Test critical workflows

### Weekly
- Update seed data
- Review performance metrics
- Optimize workflows
- Clean up old generations

### Monthly
- Update prompt templates
- Refresh approved language
- Review and update integrations
- Plan feature improvements
