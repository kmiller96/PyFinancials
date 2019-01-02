"""
The main execution of the module.

Useful for testing that the model was built correctly and to get an idea of
example functionality. There are (read: soon will be) multiple user stories
built as individual execution runs so you can see some example code in action.
"""

import openpyxl as pyxl
import pyfinancials as pf


def simple_demo():
    """A simple demo that demonstrates the current progress."""
    model = pf.FinancialModel()
    sheet = model.addSheet('MySheet')

    assumptions = sheet.addAssumptionsTable()
    assumpt1 = assumptions.addAssumption("Assumption #1", 1)
    assumpt2 = assumptions.addAssumption("Assumption #2", 2)

    section = sheet.addLineItemSection()
    lineitem1 = section.addLineItem("Line #1").equals(assumpt1 + assumpt2)
    lineitem2 = section.addLineItem("Line #2").equals(lineitem1 * assumpt1)

    model.build('demo_model.xlsx')
    return


def loan_repayment_case_study():
    """Contains the code that runs the first case study. The end goal."""
    # -- Given loan assumptions -- #
    LOAN_ASSUMPTIONS = [
        {  # -- Loan 1 -- #
            "interest_rate_pa": "10%",
            "principle": "10,000",
            "loan_length": 3,
            "compounding_freq": 1  # per year
        },
        {  # -- Loan 2 -- #
            "interest_rate_pa": "8%",
            "principle": "10,000",
            "loan_length": 3,
            "compounding_freq": 2  # per year
        },
        {  # -- Loan 3 -- #
            "interest_rate_pa": "8%",
            "principle": "10,000",
            "loan_length": 4,
            "compounding_freq": 1  # per year
        }
    ]


    # -- Build the loan repayment model. -- #
    model = pf.FinancialModel()


    # -- Build the individual calculation sheets. -- #
    for i, assumptions_dict in enumerate(LOAN_ASSUMPTIONS):
        sheet = model.addSheet("Loan #{}".format(i))
        sheet.setStyle("calculation")

        # Start with defining the assumptions for the sheet
        assumptions = sheet.addAssumptionsTable()
        interest_rate_pa = assumptions.addAssumption(
            "Interest Rate (p.a)", assumptions_dict["interest_rate_pa"]
        )
        principle = assumptions.addAssumption(
            "Principle Amount", assumptions_dict["principle"]
        )
        loan_length = assumptions.addAssumption(
            "Loan Length", assumptions_dict["loan_length"]
        )
        compounding_freq = assumptions.addAssumption(
            "Compounding Frequency (p.a.)", assumptions_dict["compounding_freq"]
        )

        # Next add the output values (i.e. the metrics)
        metrics = sheet.addMetricTable()
        repayment_metric = metrics.addMetric("Repayment Per Month")
        total_interest   = metrics.addMetric("Total Interest Paid")

        # Build the "engine" of the model.
        loan_calc   = sheet.addLineItemSection()
        som_balance = loan_calc.addLineItem("Start of Month Balance")
        interest    = loan_calc.addLineItem("Interest")
        repayment   = loan_calc.addLineItem("Repayment")
        eom_balance = loan_calc.addLineItem("End of Month Balance")

        som_balance.equals(eom_balance.previous)
        interest.equals(som_balance * interest_rate_pa/12)
        repayment.equals(repayment_metric)
        eom_balance.equals(
            pf.IF(
                repayment < som_balance + interest,
                som_balance + interest - repayment,
                0
            )
        )

        # Add some styling
        sheet.title = "Loan Repayment Calculation #{0}".format(i)


    # -- Create a dashboard page -- #
    dashboard = model.addDashboard("Summary")
    dashboard.addMetricTable(
        rows=["Loan #{}".format(i+1) for i,_ in enumerate(LOAN_ASSUMPTIONS)],
        columns=[sheet.total_interest for sheet in model.findSheets("Loan *")]
    )
    dashboard.addLineChart(
        [sheet["Start of Month Balance"] for sheet in model.findSheets("Loan *")]
    )


    # -- Compile spreadsheet -- #
    model.build("loan_calculator.xlsx")
    return


def main():
    """Executes the main, example execution."""
    return simple_demo()


if __name__ == '__main__':
    main()
