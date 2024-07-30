{ pkgs ? import (fetchTarball "https://github.com/NixOS/nixpkgs/tarball/nixos-23.11") {} }:

pkgs.mkShellNoCC {
  packages = with pkgs; [
    (python3.withPackages (ps: [
      ps.flask 
      ps.flask-cors
      ps.mysql-connector
      ps.pandas
      ps.faker
      ]))
    curl
    jq
  ];
}
