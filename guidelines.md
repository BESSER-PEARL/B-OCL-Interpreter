# Template for BESSER-PEARL Organization Repositories

The following indications assume that you have admin or owner permissions in the project.

## ☑️ Checklist

This is the list of actions you should address:

### The musts

- [ ] Edit the [Project Description](#-project-description).
- [ ] Review and adapt the [Contributing guidelines](#-contributing-guidelines).
- [ ] Review and adapt the [Code of Conduct](#%EF%B8%8F-code-of-conduct).
- [ ] Review and adapt the [Governance](#%EF%B8%8F-governance) rules.
- [ ] Choose a [License](#%EF%B8%8F-license).
- [ ] Edit the [Readme](#%EF%B8%8F-readme).

### The shoulds

- [ ] Consider clearly identifying and setting the [Code owners](#-code-owners) in your project.
- [ ] Consider using [Templates](#%EF%B8%8F-templates) for your issues/pull requests.

### The coulds

- [ ] Consider adding a [Security policy](#%EF%B8%8F-security-policy).
- [ ] Consider adding a [Fundings](#-funding) file.
- [ ] Consider using [Citation](#-citation) if you have a paper to cite your work.


## 💡 Best Practices

In the following, we cover the main elements you should configure to prepare your project. 

### 🧾 Project description

The project description is a short text which tells your community about the work you are developing. 

You can edit the project description in the `About` tab of the repository (click on the gear icon on the top right). Create a descriptive entry for the project, and include at least three tags. If the project has a website, indicate also the URL.

Finally, decide whether your repository page should include `Releases`, `Packages` or `Environments` tabs. In case of doubt, remove them. You can find more information about [Releases](https://docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository), [Packages](https://github.com/features/packages) and [Enviroments](https://docs.github.com/en/actions/deployment/targeting-different-environments/using-environments-for-deployment) in the official GitHub documentation.

### 👩‍💻 Contributing guidelines

Contributing guidelines describe how people can help with the development of your project. Is the project developed by a single contributor? Can anyone jump in and help on the development? How to send contributions? 

Contributing guidelines are generally provided in the well-known file `CONTRIBUTING.md` file.

This template includes a proposal for `CONTIBUTING.md`. Please, read carefully the provided template and adapt to your needs. Note that you will have to substitute the `YOUR-ORGANIZATION` and `YOUR-PROJECT` placeholders with the name of your organization and project, respectively.

### 👮‍♀️ Code of Conduct

The Code of conduct (CoC) of your project establishes the set of behavioral rules for the community. How harassment cases will be resolved? To whom you have to contact if you feel attacked? 

Code of conduct is often defined in the `CODE_OF_CONDUCT.md` file.

This template includes a proposal for `CODE_OF_CONDUCT.md`. Please, read carefully the provided template and adapt to your repository.

### 🏛️ Governance

Governance rules define the set of norms which are applied to make decisions in your project, and your community. On the one hand, governance project rules address questions such as: who will accept my pull request?, or how much time it will take to be accepted? On the other hand, governance community rules cover questions such as: who will accept me as part of the project leaders? 

The explicit definition of governance rules is not a trivial task, but when done, it is usually defined in the `GOVERNANCE.md` file. You can find a list of typical questions to address when defining governance rules [here](https://sustainers.github.io/governance-readiness/).

This template includes a proposal for `GOVERNANCE.md`. Please, read carefully the provided template and adapt to your repository.

### 👑 Code Owners

The code owners are those contributors that are responsible for code in your project. Thus, code owners are automatically requested for review when someone opens a pull request that modifies code that they own.

In GitHub you define the code owner in the `CODEOWNERS` file. You can find more information in the [official documentation](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners). Please, check the official documentation to be sure that write permissions in the repository are properly set.

This template includes an example proposal for `CODEOWNERS` extracted from the official documentation.  

### 🖊️ Templates

GitHub supports the definition of templates for the issues and pull requests in the project. This helps your community to better fill in these elements.

This project proposes templates for issues and pull requests. You can find them in the `.github` folder. 

* Issue templates are located in `.github/ISSUE_TEMPLATE`. You can find a template for proposals and questions, but you can modify or create new ones. You can find more information in [About issue and pull request templates](https://help.github.com/en/github/building-a-strong-community/about-issue-and-pull-request-templates). 

* Pull request template is located in `.github`. You can find more information in [About issue and pull request templates](https://help.github.com/en/github/building-a-strong-community/about-issue-and-pull-request-templates).

If you do not plan to use these templates, remove the folder. 

### ⚖️ License

The license sets the legal framework for your project. 

Check that the proposed license matches with your project. This template includes the MIT license (the standard license for public repositories of the BESSER-PEARL organization), but you can change it to any other license. You can find a list of licenses in [Choose a License](https://choosealicense.com/).

### 👮‍♀️ Security policy

Security policy describes how to report security vulnerabilities in your project. If your project does not cover this topic, you can remove the `SECURITY.md` file.

In GitHub, security policy is defined in the `SECURITY.md` file. 

This template includes a proposal for `SECURITY.md`. Please, read it carefully and adapt to your needs. You can find more information in the [official documentation](https://docs.github.com/en/code-security/getting-started/adding-a-security-policy-to-your-repository).

### 💰 Funding

Funding and sponsor indications helps your community to know how to support your work. 

In GitHub, funding and sponsor indications are defined in the `FUNDING.yml` file.

This template includes a proposal for `FUNDING.yml`. Please, read it carefully and adapt to your needs. After adapting the file, **remember to activate the sponsor button in your repository** (Settings / General / Sponsorship)

You can find more information in the [official documentation](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/displaying-a-sponsor-button-in-your-repository).

### 📓 Citation

If your work is related to a paper, and you want to facilitate its citation, review the `CITATION.cff` file. 

The provided template will help to fill the gaps, but if you need more help, you can find more information in [Citation File Format](https://citation-file-format.github.io/). Otherwise, just remove the file.

### 🗒️ Readme

As last step, modify the `README.md` file. This file summarizes your project, and normally includes sections for:

* Description: Short description of your project.
* Requirements & Installation: How to configure/install your work (if required).
* Repository structure: Describes the main elements of your repository
* Usage & Examples: Includes some usage indications and illustrative examples.
* Contributing & Governance: You can refer to `CONTRIBUTING.md` and `GOVERNANCE.md`.
* Code of Conduct: You can refer to `CODE_OF_CONDUCT.md`.
* License: You can refer to `LICENSE.md`