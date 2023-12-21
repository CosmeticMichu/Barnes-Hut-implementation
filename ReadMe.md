# Barnes-Hut implementation for 2D problem

This implementation is for solving the two dimentional N-body problem, using the acceleration structure of trees, as proposed by Barnes and Hut  in [1]. The current state of the implementation gives us interactiong bodies but it is not representing any actual physical behavior, this is due to the implementation of the physics of the problem, and this is, any the implementation of the interaction, or the implementation of the initial conditions of the bodies. 

A future update is expected to fix at least the problem with the nature of the interacting bodies (initial conditions), in order to have closed orbits, attending to a kepplerian velocities and masses in the actual range of stellar masses

[1]Barnes, J., Hut, P. A hierarchical *O(N log N)* force-calculation algorithm. *Nature*  **324** , 446–449 (1986). https://doi.org/10.1038/324446a0
