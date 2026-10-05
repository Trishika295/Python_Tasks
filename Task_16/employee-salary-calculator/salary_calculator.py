# salary_calculator.py

from salary_rules import SALARY_RULES


def calculate_allowances(basic_salary):
    """
    Calculate all salary allowances.
    """

    hra = basic_salary * SALARY_RULES["hra_percentage"] / 100

    da = basic_salary * SALARY_RULES["da_percentage"] / 100

    special_allowance = (
        basic_salary
        * SALARY_RULES["special_allowance_percentage"]
        / 100
    )

    total_allowances = hra + da + special_allowance

    return {
        "hra": hra,
        "da": da,
        "special_allowance": special_allowance,
        "total_allowances": total_allowances
    }


def calculate_gross_salary(basic_salary, total_allowances):
    """
    Calculate gross salary.
    """

    return basic_salary + total_allowances


def calculate_deductions(basic_salary, gross_salary):
    """
    Calculate salary deductions.
    """

    pf = basic_salary * SALARY_RULES["pf_percentage"] / 100

    professional_tax = SALARY_RULES["professional_tax"]

    income_tax = gross_salary * SALARY_RULES["income_tax_percentage"] / 100

    total_deductions = pf + professional_tax + income_tax

    return {
        "pf": pf,
        "professional_tax": professional_tax,
        "income_tax": income_tax,
        "total_deductions": total_deductions
    }


def calculate_net_salary(gross_salary, total_deductions):
    """
    Calculate final net salary.
    """

    return gross_salary - total_deductions


def calculate_salary(employee):
    """
    Calculate complete salary details for an employee.
    """

    basic_salary = employee["basic_salary"]

    allowances = calculate_allowances(basic_salary)

    gross_salary = calculate_gross_salary(
        basic_salary,
        allowances["total_allowances"]
    )

    deductions = calculate_deductions(
        basic_salary,
        gross_salary
    )

    net_salary = calculate_net_salary(
        gross_salary,
        deductions["total_deductions"]
    )

    salary_details = {
        "employee_id": employee["employee_id"],
        "name": employee["name"],
        "department": employee["department"],
        "basic_salary": basic_salary,

        "hra": allowances["hra"],
        "da": allowances["da"],
        "special_allowance": allowances["special_allowance"],
        "total_allowances": allowances["total_allowances"],

        "gross_salary": gross_salary,

        "pf": deductions["pf"],
        "professional_tax": deductions["professional_tax"],
        "income_tax": deductions["income_tax"],
        "total_deductions": deductions["total_deductions"],

        "net_salary": net_salary
    }

    return salary_details