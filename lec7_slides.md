# Architectural Representation

**Course:** 20H58665 - Architectural Representation
**Institution:** South China Normal University
**Instructor:** M Faizan Khan

---

## 1. Review & Outline

### Review
* Introduction to software architecture
* Architecture vs Design
* Architect's responsibilities
* Architecture Business Cycle

### Outline
* Architectural Representation using UML
* Architectural Representation using ADL (Architecture Description Language)

---

## 2. Architectural Representations Overview

### Definition
* Software architecture specifies a high level of software system abstraction by employing decomposition, composition, architecture styles, and quality attributes.
* Every software architecture must describe its collection of components and the connections and interactions among these components.
* It must also specify the deployment configuration of all components and connections.
* A software architecture design must conform to the project's functional and nonfunctional requirements.

### Box Diagrams
* **Box-and-line diagrams:** Often used to describe business concepts and processes during the analysis phase of the software development lifecycle.
* These diagrams typically come with descriptions of components and connectors, as well as other descriptions providing common intuitive interpretations.
* **Example Structure:**
    * *Catalog* ↔ *Shopping Cart*
    * *Financial Check* ↔ *Checkout* ↔ *Inventory*
    * *Checkout* ↔ *Invoice/Shipping*

---

## 3. Unified Modeling Language (UML)

### UML for Software Architecture
UML is a graphical language used for:
* Visualizing
* Specifying
* Constructing
* Documenting the artifacts of a software-intensive system.

It offers a standard way to draw a system's blueprints.

### Architecture View Models
* A **model** is a complete, simplified description of a system from a particular perspective or viewpoint.
* **Important Note:** There is no single view that can present all aspects of complex software to stakeholders.
* View models provide partial representations of the software architecture to specific stakeholders, such as:
    * System users
    * Analyst/designer
    * Developer/programmer
    * System integrator
    * System engineer
* Software designers organize the description of architectural decisions in different views.

---

## 4. The 4+1 View Model

Originally introduced by Philippe Kruchten (1995), this model is an architecture verification technique for studying and documenting software architecture design. It standardizes design documents, making them easier for all stakeholders to understand.

It consists of four essential views plus a fifth "scenario" view that ties them together:

1.  **Logical View**
2.  **Process View**
3.  **Physical View**
4.  **Development View**
5.  **Scenario View** (The "+1")

### A. The Scenario View
* **Description:** Describes the functionality of the system (how the user employs the system and how the system provides services).
* **Purpose:** Helps designers discover architecture elements during design and validate the architecture afterward.
* **Diagrams:** Supported by UML **Use Case Diagrams** and verbal documents.
    * *Example Use Case:* Passenger Service interacting with actors like Check-in Representative, Passenger, Customs, and Baggage Transportation. (Functions: Check-In, Boarding, etc.)

### B. The Logical (or Conceptual) View
* **Description:** Based on application domain entities necessary to implement functional requirements. Specifies system decomposition into conceptual entities (objects) and connections (associations).
* **Diagrams:** Supported by:
    * **Static Diagrams:** Class/Object diagrams.
    * **Dynamic Diagrams:** Interaction overview, Sequence, Communication, State, and Activity diagrams.
    * *Example Class Diagram:* Shows relationships between abstract classes (e.g., `Airplane_Abstract`) and concrete classes (e.g., `PassengerPlane`, `FighterJet`).

### C. The Development (or Module) View
* **Description:** Derives from the logical view and describes the static organization of system modules.
* **Building Blocks:** Namespaces, class libraries, subsystems, or packages that group classes for development.
* **Diagrams:** Supported by **Package Diagrams** and **Component Diagrams**.
    * *Example Package Diagram:* Shows hierarchy and dependencies between packages like `Customer`, `Cart`, `Catalog`, `Shipping`, and `Payment`.

### D. The Process View
* **Description:** Focuses on the dynamic aspects of the system (execution time behavior). Maps functions/activities to runtime implementation.
* **Concerns:** Handles concurrency and synchronization issues between subsystems.
* **Diagrams:** Supported by **Activity Diagrams** and Interaction Overview Diagrams.
    * *Example Activity Diagram:* Order processing flow (Check credit → Make shipping order/billing invoice → Save record).

### E. The Physical View
* **Description:** Describes installation, configuration, and deployment. Shows mapping of software onto hardware.
* **Concerns:** Delivery of the deployable system; specifically interesting for distributed or parallel systems.
* **Diagrams:** Supported by **Deployment Diagrams**.
    * *Example Deployment Diagram:* Shows interactions between a Web Server (running JSP/Servlets) and a Database Server via JDBC.

### F. The User Interface View (Extended)
* Provides a clear user-computer interface view, hiding implementation details.
* Can be screen snapshots or interactive prototypes.
* Modifications here directly impact the Scenario view.

---

## 5. Architecture Description Language (ADL)

### Definition
An ADL is a modeling notation to support architecture-based development. It is used to define and model system architecture *prior* to detailed design and implementation.

### Examples of ADLs
* **UML (OMG):** General-purpose
* **SADL (SRI)**
* **Aesop (Carnegie Mellon University)**
* **Acme (CMU):** Interchange format
* **Rapide (Stanford University)**
* **Wright (CMU)**
* **Darwin (Imperial College London)**

### Parts of an ADL
**Architecture Style = {Component/Connector Vocabulary, Topology, Semantic Constraints}**

1.  **Components:** Locus of computation (e.g., filter, data store, object, process, server).
    * Model principal run-time elements.
    * Have a set of **Ports** (interfaces through which components interact).
2.  **Connectors:** Interactions between components (e.g., procedure call, RPC, pipe, TCP/IP).
    * Model pathways of communication.
    * Have a set of **Roles** (specifications of behavior required of components using the connector).

### Acme: a Generic ADL
* Developed by David Garlan (CMU) and David Wile (USC).
* A simple, generic language for describing software architectures and families of architectures.
* Intended as a standard representation for tools (e.g., ACME Studio).

#### Example: Component and Connector (C&C) Model in Acme
```acme
System simple-cs = {
    Component client = { port call-rpc; };
    Component server = { port rpc-request; };

    Connector rpc = {
        role client-side;
        role server-side;
    };

    Attachments = {
        client.call-rpc to rpc.client-side;
        server.rpc-request to rpc.server-side;
    }
}