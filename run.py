"""
The main execution of the module.

Useful for testing that the model was built correctly and to get an idea of
example functionality. There are (read: soon will be) multiple user stories
built as individual execution runs so you can see some example code in action.
"""

import pyfinancials as pf


def loan_repayment_case_study():
    """Contains the code that runs the first case study."""
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
        mapper = {
            "Interest Rate (p.a)": assumptions_dict["interest_rate_pa"],
            "Principle Amount": assumptions_dict["principle"],
            "Loan Length": assumptions_dict["loan_length"],
            "Compounding Frequency (p.a)": assumptions_dict["compounding_freq"]
        }
        assumptions = sheet.addAssumptionsSection()
        for excel_name, val in mapper.items():
            assumptions.addAssumption(excel_name, initial_value=val)

        # Next add the output values (i.e. the metrics)
        repayment_metric = sheet.addMetric("Repayment Per Month")
        total_interest   = sheet.addMetric("Total Interest Paid")

        # Build the "engine" of the model.
        loan_calc   = sheet.addSection()
        som_balance = calc_section.addLine("Start of Month Balance")
        interest    = calc_section.addLine("Interest")
        repayment   = calc_section.addLine("Repayment")
        eom_balance = calc_section.addLine("End of Month Balance")

        som_balance.set(eom_balance.previous())
        interest.set(som_balance * assumptions["Interest Rate (p.a)"])
        repayment.set(repayment_metric)
        eom_balance.set(
            py.formulas.IF(
                repayment < som_balance + interest,
                som_balance + interest - repayment,
                0
            )
        )

        # Add some styling
        sheet.title("Loan Repayment Calculation #{0}".format(i))


    # -- Create a dashboard page -- #
    dashboard = model.addSheet("Summary")
    dashboard.setStyle("dashboard")

    section_table = dashboard.addSection()
    section_table.addMetricTable(
        rows=["Loan #{}".format(i+1) for i,_ in enumerate(LOAN_ASSUMPTIONS)],
        columns=[sheet.total_interest for sheet in model.findSheets("Loan *")]
    )

    section_chart = dashboard.addSection()
    line_chart = section_chart.addLineChart(
        [sheet["Start of Month Balance"] for sheet in model.findSheets("Loan *")]
    )


    # -- Compile spreadsheet -- #
    model.build("loan_calculator.xlsx")
    return


def main():
    """Executes the main, example execution."""
    return loan_repayment_case_study()


if __name__ == '__main__':
    main()
