def generate_recommendation(level):

    if level == "High":

        return {
            "Priority": "🔴 HIGH",

            "Recommendations": [

                "Arrange an immediate wellbeing meeting.",

                "Reduce employee workload.",

                "Review deadline allocation.",

                "Refer employee to wellbeing support.",

                "Monitor employee weekly."

            ]
        }

    elif level == "Moderate":

        return {

            "Priority": "🟡 MODERATE",

            "Recommendations": [

                "Discuss workload with employee.",

                "Encourage annual leave.",

                "Improve work-life balance.",

                "Review progress monthly."

            ]
        }

    else:

        return {

            "Priority": "🟢 LOW",

            "Recommendations": [

                "Maintain current wellbeing practices.",

                "Continue recognition programme.",

                "Review wellbeing quarterly."

            ]
        }
