# Implementation
## Mobis
- Requirements vs Current Completion

## Need2Do
- User input for packing list
    - Regular shipment - Low inventory of items
    - New non-regular shipment
    - What are the rates of item use?
- Sorting
    - Package importance
    - Package weight?
    - Package size
- Palletization Method
    - __*Everything* is either a container or an item__
    - New Container object
      - How much space is available?
      - Is this space smaller than the smallest package?
      - Is the total amount of free space >= to a package volume in the packing list
    - New Item object
      - Where is the package?
      - What is the package?
      - What other information is relevant to itself?
    - Order queues
        - The smallest space available is next to fill
- GUI
    - Does anyone have experience with UI design or any photo editing/creation program?

# Current Code
## Initialization
- Variable names should be descriptive
    - Exceptions exist 
        - Variables for xyz coordinates given proper comments are okay
        - Variables for iteration in small use, if you use the same iterative variable everywhere it needs a proper name

## Loops
- How many iterations are being run?
    - `iterations * length(box_dim) * V_crate`???
    - What is V_crate's ceiling?
- Worst case scenario could be hours...

## Final
- `final_matrix` doesnt do anything/isnt used??

