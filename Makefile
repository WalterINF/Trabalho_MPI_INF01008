# Makefile for MPI Matrix Multiplication

source_dir = src
build_dir = build

all: #mpi_coletiva mpi_p2p_bloqueante mpi_p2p_naobloqueante
	mpicc $(source_dir)/mpi_coletiva.c -o $(build_dir)/mpi_coletiva
	mpicc $(source_dir)/mpi_p2p_bloqueante.c -o $(build_dir)/mpi_p2p_bloqueante
	mpicc $(source_dir)/mpi_p2p_naobloqueante.c -o $(build_dir)/mpi_p2p_naobloqueante

clean:
	rm $(build_dir)/mpi_coletiva $(build_dir)/mpi_p2p_bloqueante $(build_dir)/mpi_p2p_naobloqueante
