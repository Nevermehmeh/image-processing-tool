# Makefile cho dự án Image Processor

# Biến
PYTHON = python
PIP = pip
FLAKE8 = flake8
PYTEST = pytest
BLACK = black
ISORT = isort
MYPY = mypy

# Thư mục chứa mã nguồn
SRC = app
TESTS = tests

# Lệnh mặc định
.DEFAULT_GOAL := help

# Màu sắc
RED = \033[0;31m
GREEN = \033[0;32m
YELLOW = \033[0;33m
BLUE = \033[0;34m
NC = \033[0m # No Color

# Hiển thị hướng dẫn
help:
	@echo "${BLUE}Image Processor - Các lệnh có sẵn:${NC}"
	@echo "${GREEN}make install${NC}       - Cài đặt các phụ thuộc"
	@echo "${GREEN}make dev${NC}          - Chạy ứng dụng trong môi trường phát triển"
	@echo "${GREEN}make test${NC}         - Chạy các bài kiểm tra"
	@echo "${GREEN}make lint${NC}         - Kiểm tra lỗi code với flake8"
	@echo "${GREEN}make format${NC}       - Định dạng code với black và isort"
	@echo "${GREEN}make typecheck${NC}    - Kiểm tra kiểu dữ liệu với mypy"
	@echo "${GREEN}make check${NC}        - Chạy tất cả các kiểm tra (lint, typecheck, test)"
	@echo "${GREEN}make clean${NC}        - Dọn dẹp các file tạm"
	@echo "${GREEN}make docker-build${NC}  - Xây dựng Docker image cho môi trường phát triển"
	@echo "${GREEN}make docker-up${NC}     - Khởi động các dịch vụ với Docker Compose"
	@echo "${GREEN}make docker-down${NC}   - Dừng và xóa các container"

# Cài đặt các phụ thuộc
install:
	@echo "${BLUE}Đang cài đặt các phụ thuộc...${NC}"
	$(PIP) install -r requirements.txt -r requirements-dev.txt
	@echo "${GREEN}Đã cài đặt xong các phụ thuộc!${NC}"

# Chạy ứng dụng
run:
	@echo "${BLUE}Đang khởi động ứng dụng...${NC}"
	$(PYTHON) run.py

# Chạy các bài kiểm tra
test:
	@echo "${BLUE}Đang chạy các bài kiểm tra...${NC}"
	$(PYTEST) -v --cov=$(SRC) --cov-report=term-missing $(TESTS)

# Kiểm tra lỗi code
lint:
	@echo "${BLUE}Đang kiểm tra lỗi code...${NC}"
	$(FLAKE8) $(SRC) $(TESTS)

# Định dạng code
format:
	@echo "${BLUE}Đang định dạng code...${NC}"
	$(BLACK) $(SRC) $(TESTS)
	$(ISORT) $(SRC) $(TESTS)

# Kiểm tra kiểu dữ liệu
typecheck:
	@echo "${BLUE}Đang kiểm tra kiểu dữ liệu...${NC}"
	$(MYPY) $(SRC)

# Chạy tất cả các kiểm tra
check: lint typecheck test

# Dọn dẹp các file tạm
clean:
	@echo "${BLUE}Đang dọn dẹp...${NC}"
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type d -name ".pytest_cache" -exec rm -r {} +
	find . -type d -name ".mypy_cache" -exec rm -r {} +
	find . -type f -name "*.py[co]" -delete
	find . -type f -name "*.swp" -delete
	find . -type f -name "*.swo" -delete
	find . -type f -name ".coverage" -delete
	find . -type d -name "htmlcov" -exec rm -r {} +
	find . -type d -name ".ipynb_checkpoints" -exec rm -r {} +
	find . -type d -name "dist" -exec rm -r {} +
	find . -type d -name "build" -exec rm -r {} +
	find . -type d -name "*.egg-info" -exec rm -r {} +

# Docker commands
docker-build:
	@echo "${BLUE}Đang xây dựng Docker image...${NC}"
	docker-compose -f docker-compose.dev.yml build

docker-up:
	@echo "${BLUE}Đang khởi động các dịch vụ với Docker Compose...${NC}
	Truy cập ứng dụng: http://localhost:5000"
	@echo "Truy cập pgAdmin: http://localhost:5050 (admin@example.com/admin)"
	docker-compose -f docker-compose.dev.yml up

docker-down:
	@echo "${BLUE}Đang dừng và xóa các container...${NC}"
	docker-compose -f docker-compose.dev.yml down

.PHONY: help install run test lint format typecheck check clean docker-build docker-up docker-down
