# EAA™ Architecture {#topic_ux4_zt2_jbb}

EAA™ applications rely on a number of building blocks, which can be grouped the following layers:

-   Infrastructure layer provides basic IT resources.
-   Platform as a Service\(PaaS\) layer, provides various domain-agnostic services \(platform operations, databases, and network control\)
-   Common Services layer, offering EAA™ domain specific services.

 ![](../EAA_Install_Guide_files/EAA_Functional_Architecture_1_5_E.svg "EAA™ Functional Architecture") 

## Infrastructure Layer { .section}

EAA™ applications run on any type of infrastructure, for example, a public cloud, private cloud or bare metal. The infrastructure provisioning is specific to each deployment.

## PaaS Layer { .section}

The PaaS layer offers various domain agnostic services like platform operations, databases, and network control.

## Common Services and Applications { .section}

This layer provides EAA™ domain specific services and is divided into the following families:

-   Domain-related Services and Web Applications: This includes all common components allowing for access and management to the inventories.
-   Big Data Jobs: This includes common big data analytics, which are used as part of EAA™.
-   Non-functional services: This includes transversal services such as monitoring, security \(authentication/ authorization\), and automation.

