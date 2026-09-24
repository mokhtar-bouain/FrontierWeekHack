# Synthetic FinOps Policy

All information in this document is fictional and created for the ValueLeak AI demonstration.

## General optimization policy

Cloud resources should be reviewed when sustained utilization is very low and the resource has limited business activity.

A resource with average CPU utilization below 5%, very low request volume, and no recent deployment may be considered an optimization candidate.

Low utilization alone is not sufficient evidence to stop or resize a resource.

Before recommending an action, the resource environment, criticality, operational purpose, recent activity, and applicable exceptions must be verified.

## Non-production resources

Development and test resources with sustained low utilization may be considered for scheduling, resizing, suspension, or shutdown after owner validation.

Potential savings must be calculated separately from already-incurred costs.

No automated shutdown is permitted without human approval.

## Disaster recovery exception

Resources classified as `disaster_recovery` are intentionally maintained in a ready state.

Low CPU, memory, request volume, or deployment activity is expected for these resources and must not by itself be interpreted as waste.

Disaster recovery resources marked as critical must remain available unless the Platform Team explicitly approves a change.

## Production safeguards

Production resources must not be recommended for shutdown based solely on utilization metrics.

Any optimization recommendation affecting a production resource requires additional reliability and business-impact analysis.

## Human validation

All ValueLeak recommendations are advisory.

Stopping, resizing, deleting, or reconfiguring a cloud resource requires explicit human validation.
