fn main() {
    let path = std::env::args().nth(1).unwrap();
    let txt = std::fs::read_to_string(path).unwrap();
    let bytes = thox_patch_loader::canonical_bytes(&txt).unwrap();
    std::fs::write("/tmp/canon_rs.bin", &bytes).unwrap();
    println!("{}", String::from_utf8_lossy(&bytes));
}
