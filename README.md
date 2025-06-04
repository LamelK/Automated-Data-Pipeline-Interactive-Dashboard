# Automated-Data-Pipeline-Interactive-Dashboard# Automated Data Pipeline with Secure Dashboard Access  

## Overview  
This project automates the process of collecting, processing, and visualizing data using AWS cloud services.The pipeline efficiently ingests raw data, performs ETL (Extract, Transform, Load) operations, and creates interactive dashboards for data-driven insights 

The goal is to demonstrate hands-on cloud engineering and data analytics skills by designing and implementing a complete data solution from automating ETL workflows to building interactive, insightful dashboards for analysis and reporting.

---

## Architecture  
<img src="my_0architecture_diagram.png" alt="Pipeline Diagram" width="700"/>


### Key Components  
| AWS Service       | Purpose                                  |  
|-------------------|------------------------------------------|  
| EventBridge       | Weekly cron trigger                      |  
| Step Functions    | Orchestrates data workflow               |  
| Lambda            | Extract,Transform,Load |  
| S3 + VPC Endpoint | Secure intermediate storage              |  
| RDS (MySQL)       | Structured data storage                  |  
| EC2 (Metabase)    | Dashboard hosting                        |  

---

## Access Control  
**Application URL**: 🔒 [https://insightportals.fyi/](https://insightportals.fyi/)  

This application requires me to create a user account for you before you can access the dashboard, it’s set up for team-based access

**Request access **:  
✉️ [Lamel466@gmail.com](mailto:Lamel466@gmail.com)    

---

## Technical Documentation  
For detailed documentation, please refer to the PDF.

---

## Data Flow  
<img src="SEQUENCE_DIAGRAM.jpg" alt="Process Steps" width="900"/>  
1. **Trigger**: Weekly EventBridge cron  
2. **Extract**: Mockaroo API   
3. **Transform**: Step Functions workflow → Lambda → S3
4. **Load**: Lambda → RDS (private subnet)  
5. **Visualize**: Metabase dashboards  


By integrating serverless architecture and secure VPC networking, this design delivers a scalable, cost-effective, and maintainable data pipeline. The final result is an automatically updated, interactive dashboard providing fresh data insights every Monday without manual intervention.
---

