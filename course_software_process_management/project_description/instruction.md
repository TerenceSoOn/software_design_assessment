As a newly formed group, you must finalise your project and write a project
description (regarding the problem to be solved and potential features of the
proposed software). The project specification document is required to be a
short document (a maximum of 2 pages) that should explain the problem and
the key potential features that the project should emphasise (see the exemplar
project/specification document provided at the end of this page).

You can choose any projects you would have done as part of your previously
completed courses (such as "JC2001: Introduction to Software Engineering) or
any new project idea that you feel is appropriate to complete this activity.

---

## Exemplar Project Scenario 1 (for "Customer Relationship Management Software" [1])

### 1. Problem Statement

A Customer Relationship Management (CRM) provider, Sell-IT, has fallen behind and failed to right
itself after being outpaced in features and services by other competitors. After cleaning the house, the
new CEO has hired your team to completely rewrite their existing and outdated CRM product, trying
to emulate a start-up culture. They hope to increase their clients' satisfaction, implement easier use of
the system, attract more high-profile clients, and provide an in-depth analysis of system functions, for
both the business itself and its clients. The CEO wants the new system to be cutting-edge and
competitive, as well as easy to use and maintain. The new system must be able to be marketed and
deployed as a minimum viable product as soon as possible. At this time, there are several enterprise
systems that the existing clients rely upon, making it necessary that the new product be designed with
built-in integrations. This is a trend throughout the CRM industry and will need to be maintained. The
old system had these integrations but also included a hard set of features, some of which some clients
never used and couldn't remove; the CEO wants the new system to have modular features which can
be built up over time. This will allow the business to cater and shape product instances to a client's
needs, as well as sustain the business through future features. The requirements for this system are
given in the list below as either minimum viable features or desired features for the overall system.
The list is neither exhaustive nor definitive. It is up to your team to develop a list of features that best
fit the scope of your application. Remember, the feature set is meant to be modular, and this company
is currently in flux, so new features and their priorities could be added, removed, or changed.

### 2. Minimum Viable Features (MVF)

a) **Workflows:** The new product must provide workflows for as many system tasks as possible,
such as data collection, analysis (Desired Feature), and marketing tasks.

b) **Contact & Sales Management:** The new product must allow clients to manage their customers
& potential customers and track purchases of client products & services. They must be able to
organize these elements [customers, purchased products & services, and potential customers]
into groups with personalization features, metadata tags for filtering, analytics, and event &
message notifications organized by group and element type.

c) **Salesforce, SharePoint, & Oracle ERP (HR) Integration:** The new product must be able to
integrate with legacy installations of Salesforce, SharePoint, & Oracle ERP. This integration
includes Single Sign On, seamlessly exporting and importing data in real-time, and accessing
some of the other systems' features from the new Sell-IT product.

### 3. Desired Features

a) **Sales Analytics & Forecasting:** The new product must have the capability of collecting data
from various website traffic, social media, and the system itself to analyse marketing
performance, anticipated revenue, and uncontacted potential customers for clients. This
forecasting could be accomplished by developing or procuring an AI engine geared towards
this function. The results of any analysis and the aggregated data must be displayed in an easy-
to-use, filterable dashboard.

b) **Email Integration & Analytics:** Integrating Outlook, Gmail, etc into the new product would
make it very attractive for clients who communicate with a wide range of customers. Including
analytics on email and email content from clients' customers would also provide valuable
insights and increase desired feature #1's forecasting accuracy.

c) **Additional Workflows:** Create optimized workflows for marketing, customer sign-on, data
retrieval, data analysis, and reporting. These are the CEO's current ideas for some workflows,
organized by category (they will vary in complexity):

   i. **Marketing:**
   - Creating marketing plans
   - Reviewing & approving/rejecting marketing plans
   - Disseminating marketing plans

   ii. **Customer sign-on:**
   - Identifying and contacting a potential customer
   - Proof of Concept sign-off, planning, & tracking (for point of contact)

   iii. **Data retrieval:**
   - Retrieve data from:
     - Ad views & clicks
     - Purchasing/Pricing page views
     - Social media views
     - News mentions

   iv. **Data analysis and Reporting:**
   - Perform analysis.
   - Make analysis available for reporting.
   - Generate specialized reports.

d) **Automation:** Automating certain aspects of the sales process workflow for clients & clients'
customers would make the product much more competitive. Including these automations with
MVF#3's external system integrations would increase clients' productivity.

e) **Lead Management:** A possible expansion and utilization of analysis capabilities, the system
could save or even programmatically determine the best customers for a given client through
analysis of psychographic factors as well as demographics. This would increase productivity
and likely increase successful sales & marketing campaigns. Remember, these are suggestions.
Feel free to add to or modify these requirements based on the design of your system, research,
and domain analysis. Your instructor may assist you and clarify if need be.

---

## Exemplar Project Scenario 2 (for "State Metro System" [2])

### 1. Problem Statement

Your local metro service has recently been re-evaluating and upgrading various components in their
metro system. As part of this initiative, they have reached out to your team to redesign their current
software. They hope to reduce employee training overhead and streamline their processes, resulting
in higher employee productivity and overall better metro service to the public. They want a more
robust system designed around their specific needs, as opposed to trying to make their current set-up
work for them. The new system must be user-friendly and able to replace the current software set-up
in a consolidated, efficient manner.

Currently, there are different software systems for various metro system needs, each with specific
hardware requirements and each requiring separate accounts and sign-on. This is extremely
inconvenient for employees that fulfil multiple roles and makes monthly metrics gathering lengthy and
difficult. Management spends an unreasonable amount of time trying to manage and coordinate
accounts, particularly during employee turnover, and the ramp-up time for employee training is too
long. The stand-alone systems themselves serve their functions well, but using the various systems
together has been a struggle.

Finally, the current repair management system is extremely basic and does not provide all the features
desired by the repair team and upper management. Employees commonly just log repair and inventory
information by hand. Periodic inspections are completed and are loosely documented unless action
needs to be taken.

The requirements for this system are given in the list below as desired features for the overall system.
The list is neither exhaustive nor definitive. It is up to your team to develop a list of features that best
fit the defined scope of your application.

### 2. Potential Features

a) **Train Coordination:** As the most public-facing aspect of the metro system, there must be some
application component to view and manage the trains themselves. The primary objective is
always passenger safety, closely followed by the desire for an optimized system. The train
coordination would encompass tracking and communicating with individual trains, as well as
finding optimized routes. The system should be able to re-calculate optimal routes in case of
repairs to a section of track, closed city blocks, or any emergency. Information on the current
trains should be visible and may include the current number, location, and status of trains.
Some goals for this portion of the application should be maximized efficiency, availability, and
security.

b) **Employee Management/Administration:** The customer is also concerned with the low
usability and efficiency of the current employee management/administration system. The
component should have different views for employees versus managers, since employees will
primarily use this system for timekeeping whereas management may additionally use it for
any tasks concerned with managing their reportees. This includes viewing and managing
assignments, approving weekly time logs, and viewing metrics. There may be different views
depending on what level of management the user is at (e.g. direct managers care about time
and tasks for a small group of people, whereas higher management would want larger metrics,
statistics, and graphs).

c) **Ticket Purchasing:** There may be two views to facilitate ticket purchasing - one for user self-
serve kiosks and one for employees at a booth aiding customers. The system should be able
to accommodate any permanent or temporary changes in tickets and ticket pricing, including
any discounts and promotions. A more advanced feature may include an external public online
or mobile application allowing riders to pre-purchase tickets, add money to a metro card, or
do other tasks at their convenience.

d) **Maintenance & Repair Management:** Another important suggested component of the system
is a sub-component for managing all metro system repairs. This may include an inventory of
all trains, rails, and replacement parts, and should provide easy links to purchase more. It
would also be beneficial to have a system to log, monitor, and manage maintenance requests,
sorted by priority, severity, and status. Maintenance requires dedicated man-hours, which is
associated with employee time tracking in the employee administration component.

e) **Dashboard View:** Finally, the customer would like a central location to view all statistics,
metrics, and graphs associated with the entire system. This includes (but is not limited to) the
suggested metrics from previous sections and any other useful information. The system should
have the capability to produce a formal report from this view, so the metro service can easily
provide quantitative status reports at meetings with other corporate partners.

---

## Exemplar Project Scenario 3 (for "Water Monitoring and Alert System" [3])

### 1. Problem Statement

Over the years the Island of American Samoa has seen economic and environmental devastation. Most
recently, the island was hit by a Tsunami that destroyed property over a mile inland. A non-for-profit
foundation, funded in great part by several NFL players of Samoan descent, has created a grant to
implement a general purpose Water Monitoring and Alert System (WMAS). Their primary goal is to be
able to deploy, configure and monitor remote-sensing buoys around the island waters that will operate
in conjunction with a diagnostic and alert station. Among other things, this system will facilitate the
monitoring of wave patterns, the forecast of dangerous water conditions and the emergency broadcast
of alerts to the island inhabitants. Clients will be able to manage and configure the initial central station
and monitor the island waters via control software. They will be able to enable and disable buoys
onboard computers and their sensors via remote connection. Operators should also be able to retrieve
previously stored data from the system and examine and map the information about any of the buoy's
sensors. The systems should also allow for expanding the number of locations and buoys monitored
and diagnosing their status remotely. The users will start with your general solution and be able to
configure the product to meet their specific needs.

As part of the alert system, your software must be able to also run autonomously and analyse data
based on pre-established thresholds. Exceeding these thresholds will trigger the alert system which is
run by a third party.

The requirements for this system are given in the list below as desired features for the overall system.
The list is neither exhaustive nor definitive. It is up to your team to develop a list of features that best
fit the defined scope of your application.

### 2. Potential Features

a) **Buoy Sensors**

   i. The buoy sensors are typically deployed by retrofitting industrial buoys with
   corresponding devices. These devices capture water temperature, GPS location,
   degree of activity (gyroscope) as well as digital images and sound.

   ii. New types of sensors are being developed to be able to capture other types of data
   and your system must account for enhancements like these in the future.

   iii. The sensors capture data and store it at configurable intervals. They transmit the
   data based on a programmed schedule by communicating to Sensor Station(s).

b) **Sensor Stations**

   i. Sensor stations are deployed in the proximity of the beach area being monitored.
   Powerful antennas and the corresponding hardware are deployed by a third party
   and hooked to a computer network connected to the central station where your
   software solution will run.

c) **Central Station**

   i. Central station is the focal point for all data storage and data mining. The physical
   structure is already being expanded from a building previously constructed for the
   island's weather forecasting and radio broadcasting station. Facilities have been
   allocated to host your hardware and provide a comfortable environment for the
   operators. Powerful antennas and the corresponding hardware are deployed by a
   third party and hooked to a computer network connected to the central station
   where your software solution may run.

   ii. Power and networking infrastructure is already in place but your system must be
   able to account for bringing the system online as soon as possible if a power outage
   occurs and allow for remote access to the system.

d) **Administration**

   i. Can add and configure new stations and buoys to the WMAS
   ii. Be able to filter data coming from specific location(s)
   iii. Control access of specific users to specific locations
   iv. Report on critical events. (i.e. sensor stops transmitting; buoy appears not to be
   moving, etc.)

e) **Monitoring**

   i. Given appropriate access, users can monitor the status/mapping of sensor data in
   your solutions GUI.
   ii. Users can retrieve historical data and created reports and produce weather maps.

---

## References

[1] 'SWEN 256 - Software Process and Project Management'. Accessed: Feb. 17, 2024. [Online].
Available: https://www.se.rit.edu/~swen-256/projects/scenarios/scenario1.html

[2] 'SWEN 256 - Software Process and Project Management'. Accessed: Feb. 17, 2024. [Online].
Available: https://www.se.rit.edu/~swen-256/projects/scenarios/scenario3.html

[3] 'SWEN 256 - Software Process and Project Management'. Accessed: Feb. 17, 2024. [Online].
Available: https://www.se.rit.edu/~swen-256/projects/scenarios/scenario5.html