# ----------------------------------------------------------------------
# Integration & Wiring – Wave 2
# ----------------------------------------------------------------------
def setup_integration(registry, optimizer, critic, spawner, verifier, msg_pool):
    """
    Wire together the core components for Wave 2.
    """
    # 1. Auto‑inject skills into the grind spawner
    if hasattr(registry, "auto_inject_into_spawner"):
        registry.auto_inject_into_spawner(spawner)

    # 2. Attach prompt optimizer (few‑shot examples) to the spawner
    if hasattr(optimizer, "attach_to_spawner"):
        optimizer.attach_to_spawner(spawner)

    # 3. Connect critic to task verification
    if hasattr(verifier, "original_verify"):
        verifier.original_verify = verifier.verify  # preserve original
    verifier.critic = critic
    verifier.verify = verifier.verify_with_critic.__get__(verifier, verifier.__class__)

    # 4. Register workers with the message pool
    if hasattr(spawner, "workers"):
        for worker in spawner.workers:
            msg_pool.register_worker(worker)

    # Expose the pool to workers that need it
    for worker in spawner.workers:
        if hasattr(worker, "set_message_pool"):
            worker.set_message_pool(msg_pool)

    print("[Integration] Wave 2 wiring complete.")