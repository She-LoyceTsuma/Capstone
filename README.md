# Fraud Detection System
This is a fraud detection system that uses predicive modeling to determine whether an insuraance clain is fradulent.

## Business Understanding

** Key Business Questions: 
##### How can fraud be identified more efficiently?
The system will remove human bias that can alter the decision-making process.
##### What are the cost savings and risk reductions that the system provides?
Reduces the cost and time taken to make decisions, data-driven decisions. 
##### How can the system improve stakeholder’s trust and the fairness of premium pricing?
Users can be informed if their accounts have been marked as fraudulent, and they don’t have to remove bribes to get their insurance claims met. 
##### What technologies can be leveraged to enhance fraud detection?
 Consider implementing machine learning algorithms, real-time analytics, and behavioral biometrics. These technologies can analyze patterns and anomalies in data, improving detection rates without relying on human judgment.
##### What metrics will be used to measure the system's effectiveness in fraud detection?*
 Key performance indicators (KPIs) such as false positive rates, detection speed, and overall fraud loss recovery rates can help assess the system's efficiency and effectiveness.
##### How will the system adapt to evolving fraud tactics?
 Incorporating adaptive learning algorithms that update based on new fraud patterns and data inputs ensures the system remains effective against emerging threats.


## Data Understanding
The dataset, named "insurance_claims.csv", is a comprehensive collection of insurance claim records. Each row represents an individual claim, and the columns represent various features associated with that claim. The dataset is, highlighting features like 'months_as_customer', 'age', policy_number, etc. The main focus is the 'fraud_reported' variable, which indicates claim legitimacy. Claims data were sourced from various insurance providers, encompassing a diverse array of insurance types including vehicular, property, and personal injury. Each claim's record provides an in-depth look into the individual's background, claim specifics, associated documentation, and feedback from insurance professionals.
Dataset Composition:
Data origin :Mendley.com
Total Records: 1,000
Number of Features : 39 
Target column : Fraud detected
![image](https://github.com/user-attachments/assets/b3ce0475-10b8-406a-967c-375a64b86c53)


The model has a high sensitivity of about 67%. It implements logistic regression to classify whether an insurance claim is fradulent or not. 
