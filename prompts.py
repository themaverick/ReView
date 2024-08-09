prompt1 = r"""You are an advanced language model tasked with analyzing customer reviews for a specific product. The reviews include a rating out of 5, a title, and the main body of the review. Your objective is to extract meaningful insights that will help a potential buyer make an informed decision about whether to purchase the product. Your analysis should provide:

Overall Sentiment Analysis:

Summarize the general sentiment of the reviews (positive, negative, or mixed).
Highlight any patterns or trends in the ratings (e.g., most reviews are 4 stars, consistent 5-star ratings, frequent 1-star complaints).
Pros:

Identify and list the most common positive aspects mentioned by reviewers.
Provide specific examples of features, qualities, or experiences that customers appreciated.
Cons:

Identify and list the most common negative aspects mentioned by reviewers.
Highlight any recurring issues, complaints, or dissatisfaction points raised by multiple reviewers.
Key Insights:

Extract any additional insights that do not fall strictly under pros or cons but are important for understanding the product (e.g., variations in product performance, unique use cases, or specific customer needs addressed).
Note any discrepancies between high ratings and negative comments or low ratings with positive comments.
Decision-Making Summary:

Provide a final summary that encapsulates the overall crux of the reviews.
Offer a balanced view that weighs the pros and cons to assist the potential buyer in making an informed decision.
Input Format:

Rating: [Rating out of 5]
Title: [Title of the review]
Body: [Body of the review]
Output Format:

Overall Sentiment Analysis:
[Summary of general sentiment and rating trends]
Pros:
[List of pros with examples]
Cons:
[List of cons with examples]
Key Insights:
[Additional important insights]
Decision-Making Summary:
[Balanced summary to aid in decision-making]
Here are the reviews: \n {structuredReviews}
"""

prompt2 = r""" 
        Convert the following report into a well-structured HTML page. 
        Ensure that the content remains unchanged and that all sections and subsections are preserved. 
        Use appropriate HTML tags to represent the structure of the document, including headers for sections, 
        paragraphs for text, and lists where applicable. Maintain the hierarchy of the sections and subsections as they appear in the original report.
        DO NOT USE '\n'
        Here is the report: \n {report}
"""