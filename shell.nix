{ pkgs ? import <nixpkgs> {} }:
pkgs.mkShell {
  nativeBuildInputs = with pkgs; [
    python312Packages.pygame
    python312Packages.numpy
  ];
}
