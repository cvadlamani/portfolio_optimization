def optimize_portfolio(Hamiltonian_matrix, stocks):
    import time
    import numpy as np
    from parameters import K_PRIME, N_SAMPLES, ALPHA
    from qci_client import QciClient

    # Start timing the function execution
    beg_time = time.time()

    K = len(stocks) # Total no.of stocks

    # Ensure the Hamiltonian matrix dimensions match the number of stocks
    assert Hamiltonian_matrix.shape[0] == K
    assert Hamiltonian_matrix.shape[1] == K

    # Generate the constraint vector for the optimization problem                                                               
    constraints_lhs = np.ones(shape=(K), dtype=np.float32)
    constraints_rhs = np.array([-K_PRIME])
    constraints = np.hstack([constraints_lhs, constraints_rhs])

    # Create JSON objects for the objective function and constraints 
    objective_json = {
        "file_name": "objective_function.json",
        "file_config": {
            "objective": {"data": Hamiltonian_matrix, "num_variables": K},
        }  
    }
    
    constraint_json = {
        "file_name": "constraints.json",
        "file_config": {
            "constraints": {
                "data": constraints, 
                 "num_variables": K,
                 "num_constraints": 1,
            }
        }
    }

    
    ## Initialize the QCI client and upload the objective and constraint JSON files
    token = "8982feb60ad44ce68ba981ad7a9970b7"
    api_url = "https://api.qci-prod.com"
    qci = QciClient(api_token=token, url=api_url)

    response_json = qci.upload_file(file=objective_json)
    objective_file_id = response_json["file_id"]

    response_json = qci.upload_file(file=constraint_json)
    constraint_file_id = response_json["file_id"]

    # Define job parameters for the optimization job
    job_params = {
        "device_type": "dirac-1", 
        "alpha": ALPHA, 
        "num_samples": N_SAMPLES,
    }
    
    # Build the job JSON body to submit the optimization job
    job_json = qci.build_job_body(
        job_type="sample-constraint", 
        job_params=job_params,
        constraints_file_id=constraint_file_id, 
        objective_file_id=objective_file_id,
        job_name=f"Portfolio Optimization",
        job_tags=["portfolio stock optimization"],
    )
    
    
    # Submit the optimization job and retrieve the job response
    job_response_json = qci.process_job(
        job_body=job_json
    )

    
    # Extract results from the job response
    results = job_response_json["results"]
    energies = results["energies"]
    samples = results["solutions"]
    is_feasibles = results["feasibilities"]

    # # Find the feasible solution with the lowest energy (objective value)                                               
    solution = None
    for i, item in enumerate(samples):
        solution = item
        is_feasible = is_feasibles[i]

        if is_feasible:
            break

    # Check if a feasible solution was found
    if not is_feasible:
        print("Solution is not feasible!")
    # Assert that the solution size matches the number of stocks
    assert len(solution) == K, "Inconsistent solution size!"
    # Check if the number of selected stocks matches the expected number
    if sum(solution) != K_PRIME:
        print(
            "Expected to select %d stocks, but selected %d!"
            % (K_PRIME, sum(solution))
	)

    # Determine which stocks are selected based on the solution vector
    selected_stocks = []
    for i in range(K):
        if solution[i] > 0:
            selected_stocks.append(stocks[i])
    # Print the time taken to complete the optimization
    print(
        "In optimize_portfolio; done with checking constraints; %0.2f seconds!"
        % (time.time() - beg_time)
    )
    # Return the binary solution vector and the list of selected stocks
    return solution, selected_stocks