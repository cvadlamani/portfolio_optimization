def optimize_portfolio(Hamiltonian_matrix, stocks):
    import time
    import numpy as np
    from parameters import K_PRIME, N_SAMPLES, ALPHA
    from qci_client import QciClient

    beg_time = time.time()

    K = len(stocks)

    assert Hamiltonian_matrix.shape[0] == K
    assert Hamiltonian_matrix.shape[1] == K

    # Generate the constraint                                                                
    cons_lhs = np.ones(shape=(K), dtype=np.float32)
    cons_rhs = np.array([-K_PRIME])

    constraints = np.hstack([cons_lhs, cons_rhs])

    # Create json objects   
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

    
    # Solve the optimization problem
    token = "8982feb60ad44ce68ba981ad7a9970b7"
    api_url = "https://api.qci-prod.com"
    qci = QciClient(api_token=token, url=api_url)

    response_json = qci.upload_file(file=objective_json)
    objective_file_id = response_json["file_id"]

    response_json = qci.upload_file(file=constraint_json)
    constraint_file_id = response_json["file_id"]

    job_params = {
        "device_type": "dirac-1", 
        "alpha": ALPHA, 
        "num_samples": N_SAMPLES,
    }
    
    job_json = qci.build_job_body(
        job_type="sample-constraint", 
        job_params=job_params,
        constraints_file_id=constraint_file_id, 
        objective_file_id=objective_file_id,
        job_name=f"Portfolio Optimization",
        job_tags=["portfolio stock optimization"],
    )
    print(job_json)
    
    job_response_json = qci.process_job(
        job_body=job_json
    )

    print(job_response_json)

    results = job_response_json["results"]
    energies = results["energies"]
    samples = results["solutions"]
    is_feasibles = results["feasibilities"]

    # The sample solutions are sorted by energy                                               
    sol = None
    for i, item in enumerate(samples):
        sol = item
        is_feasible = is_feasibles[i]

        if is_feasible:
            break

    if not is_feasible:
        print("Solution is not feasible!")

    assert len(sol) == K, "Inconsistent solution size!"

    if sum(sol) != K_PRIME:
        print(
            "Expected to select %d stocks, but selected %d!"
            % (K_PRIME, sum(sol))
	)

    sel_stocks = []
    for i in range(K):
        if sol[i] > 0:
            sel_stocks.append(stocks[i])

    print(
        "In optimize_portfolio; done with checking constraints; %0.2f seconds!"
        % (time.time() - beg_time)
    )

    return sol, sel_stocks