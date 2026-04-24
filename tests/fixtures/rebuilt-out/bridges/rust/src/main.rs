mod a0_qk_constants;
mod a1_at_functions;
mod a2_mo_composites;
mod a3_og_features;
mod a4_sy_orchestration;

fn main() -> Result<(), Box<dyn std::error::Error>> {
    a4_sy_orchestration::bridge_main::run()
}
