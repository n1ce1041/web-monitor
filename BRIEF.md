Aiven SRE Coding Challenge
==========================

This is a coding exercise for Site Reliability Engineering positions at Aiven.

The assignment is structured to take a weeknight or two, but you can spend as much or as little time as you like. If you run out of time, please return a partial solution implementing the parts you consider most essential, and describe how you would continue if you had more time. An item in a TODO bullet list can go a long way to show that you're aware of a shortcoming. 

Process
-------

You have been given access to this GitHub repository. It is currently empty bar these instructions. Create a PR with your implementation and mark it as ready when you are finished. An Aiven engineer will then go through the PR and provide feedback. You have the opportunity to respond, but we do not expect you to spend more time implementing the requested changes.

Task
----

Aiven wants to create an example Python program which uses our services. This example code needs to be a usable tool for Python developers to read, copy, or use in any way they see fit. The task is to create a scalable web monitor application that feeds information about website availability to an Aiven Kafka instance. It will act as a producer that periodically checks target websites for their status and sends the results to a Kafka topic.

The website checker should perform website status checks periodically and collect:

- Total response time
- HTTP status code, if the request completes successfully
- Whether the response body matches an optional regex check that can be passed as config to the program

This info should be written to the Kafka topic for later consumption.

Using Aiven Services
--------------------

You will need to use Aiven hosted services to complete this task. You can sign up at https://console.aiven.io/signup for a new account and receive $300 of free credit to try out our services (you are not required to provide any payment method). This should be enough for the assignment, but if you run out of credits, please let us know and we will take care of it.

When you are finished developing, please shut down any services you have started. We will launch our own services to test your code during the evaluation process.

How we will (not) use your code
-------------------------------

Please note that the scenario described below is entirely hypothetical and has been contrived purely for the sake of this assignment. This code will not be used for production or demo purposes. It will only be used in the recruitment and candidate evaluation process.

Presentation
------------

The target audience for this demo includes high-level engineering staff at client organizations. As such, we expect the quality of the code and the repository surrounding it to reflect well on Aiven. Even though this is a demo, readable code, clear documentation, clean commit history, and proper project metadata are very important. The repository should look like a well-maintained open source project, only smaller.

Things to consider
------------------

Remember the audience for this assignment at all times: a standard Python developer that's looking to use Aiven to meet their organization's needs. This repository should be clear for an engineer of any level to read, but it should also hold up to scrutiny from experienced engineers.

Fit your solution to the scenario. We understand that you may want to show off your knowledge in a particular library or technology, but if they do not suit the scenario, it's best to leave them out. Over-engineered solutions, or excessive implementations will be viewed negatively. While the list of things to prioritize is ultimately up to you, the following items are worth considering:

- An average Python developer should be able to get this code working on an Aiven service of their own by following the instructions you give.
- Simple, clear implementations that make use of common libraries are more useful than involved, complex implementations. Readability counts.
- It's good to take some time to think about the problem before coding. In the real world, events don't always go down the happy path. Production code should be able to account for this, within reason.

Do not assume Docker or any particular container platform for this assignment, and do not require complicated builds to get code running. Essentially, this code should be runnable with a standard Python setup and a tool for installing Python-level packages. Remember, it's intended to be easy-to-run for Python developers everywhere.

Evaluation criteria
-------------------

To evaluate your submission we will check out your code, read it for clarity, and attempt to configure it and run it against an Aiven service on our end. We will use the following criteria to judge your work:

- *Completeness*: Is the assignment complete according to the described scenario? Does it work?
- *Security*: Does the code expose users to vulnerabilities? Does the repository expose things to the public that should be private?
- *Robustness & Reliability*: How well does this handle real-world situations?
- *Hygiene & Maintainability*: Is the repository well-structured? Is the code easy to read? Do tests cover relevant parts?
- *Scalability & Simplicity*: Can the program scale to a larger number of websites without gaining an unmaintainably complex implementation?
- *Automation & Documentation*: Is the program easy to install, configure, and get running based on the given documentation and tools?
- *Open source-readiness*: Is this ready to publish in a public open source repo? Are any examples from other open source code attributed properly?
