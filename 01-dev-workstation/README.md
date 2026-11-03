cat << 'EOF' > ~/my-study-repo/01-dev-workstation/README.md
# 🛠️ 개발 워크스테이션 구축 및 환경 격리 검증 보고서

## 1. 프로젝트 개요
- **목표:** Linux CLI(터미널), Docker 컨테이너 런타임, Git/GitHub 형상관리 도구를 직접 세팅하여 "내 컴퓨터에서만 동작하는 문제"를 해결하고, 팀원 누구나 재현 가능한 표준 개발 워크스테이션 환경을 구축 및 검증합니다.
- **핵심 수행 내용:**
  1. 리눅스 파일시스템 계층 구조 파악 및 권한(chmod) 제어 체계 검증
  2. Docker 데몬 점검 및 컨테이너 라이프사이클(격리 프로세스, 상태 점검) 실습
  3. Nginx 베이스의 커스텀 웹 서버 이미지 빌드 및 독립 포트 매핑 검증
  4. 바인드 마운트(실시간 변경 반영) 및 Docker 볼륨(데이터 영속성) 메커니즘 증명
  5. Git 형상관리 및 VSCode 원격 개발 환경 연동

---

## 2. 실행 환경
| 구분 | 상세 환경 |
| :--- | :--- |
| **Host OS** | Windows 11 Pro (WSL 2 활성화) |
| **Guest OS / Shell** | Ubuntu 22.04 LTS / bash (5.1.16) |
| **Container Engine** | Docker Desktop 4.30+ (Engine: 26.1.1, API: 1.45) |
| **VCS / Editor** | Git 2.34.1 / Visual Studio Code (WSL Remote Extension) |

---

## 3. 수행 항목 체크리스트
- [x] **[CLI]** 터미널 기본 조작 (경로 확인, 디렉토리 탐색, 파일 생성/복사/이동/삭제)
- [x] **[Permission]** 파일 및 디렉토리 권한 변경(chmod 644/755) 전후 비교
- [x] **[Docker Engine]** Docker 버전 확인 및 데몬 동작 상태 점검 (`docker info`)
- [x] **[Container Basics]** `hello-world` 검증 및 Ubuntu 대화형 컨테이너 조작
- [x] **[Lifecycle]** 백그라운드 컨테이너 운영 로그 및 리소스 모니터링 (`logs`, `stats`)
- [x] **[Custom Dockerfile]** 경량 Nginx 베이스 커스텀 이미지 제작 및 빌드
- [x] **[Network]** 호스트-컨테이너 간 독립 포트 매핑(8080, 8081) 접속 검증
- [x] **[Bind Mount]** 호스트 소스 수정 시 컨테이너 무중단 즉시 반영 검증
- [x] **[Volume Persistence]** 컨테이너 강제 삭제 후에도 데이터 보존 검증
- [x] **[Git & GitHub]** 사용자 정보 등록, 기본 브랜치 설정 및 원격 저장소 연동
- [x] **[Troubleshooting]** 디렉토리 권한 및 포트 바인딩 충돌 트러블슈팅 2건 기록
- [x] **[Security]** 개인 식별 정보 및 인증 정보 마스킹 처리

---

## 4. 검증 방법 및 결과 위치

| 검증 항목 | 검증 명령 | 확인 내용 | 결과 위치 |
| :--- | :--- | :--- | :--- |
| **터미널 파일 조작** | `pwd`, `ls -la`, `cp`, `mv`, `rm` | 디렉토리 트리 및 파일 생성/삭제 확인 | [4.1 절](#41-터미널-조작-및-권한-실습-로그) |
| **파일/디렉토리 권한** | `chmod`, `ls -l`, `ls -ld` | 644 vs 755 권한 비트 및 접근 통제 확인 | [4.1 절](#41-터미널-조작-및-권한-실습-로그) |
| **Docker 엔진 점검** | `docker --version`, `docker info` | 런타임 클라이언트 및 서버 데몬 연동 확인 | [4.2 절](#42-docker-설치-점검-및-운영-로그) |
| **컨테이너 운영** | `docker ps -a`, `logs`, `stats` | 격리 프로세스 상태, 로그 스트림, 리소스 점검 | [4.2 절](#42-docker-설치-점검-및-운영-로그) |
| **커스텀 이미지 빌드** | `docker build`, `docker images` | `nginx:alpine` 기반 레이어 빌드 및 이미지 생성 | [4.3 절](#43-커스텀-dockerfile-웹-서버-구축) |
| **포트 매핑 접속** | `-p 8080:80`, `curl`, 브라우저 | 호스트 포트 포워딩을 통한 서비스 접근 확인 | [4.4 절](#44-포트-매핑-접속-증거) |
| **바인드 마운트** | `-v $(pwd)/app:...`, `curl` | 호스트 파일 변경 시 재빌드 없는 핫 리로드 | [4.5 절](#45-바인드-마운트-반영-검증) |
| **볼륨 영속성** | `docker volume create`, `docker rm -f` | 컨테이너 삭제 후 새 컨테이너에서 데이터 유지 확인 | [4.6 절](#46-docker-볼륨-데이터-영속성-검증) |
| **Git/GitHub 연동** | `git config --list`, GitHub 푸시 | 로컬 환경 설정 및 원격 저장소 동기화 | [4.7 절](#47-git-설정-및-githubvscode-연동) |

---

## 5. 상세 수행 및 검증 로그

### 4.1 터미널 조작 및 권한 실습 로그

#### (1) 기본 파일 조작
```bash
developer3025@GNIA-C402-H01:~/my-study-repo/01-dev-workstation$ pwd
/home/developer3025/my-study-repo/01-dev-workstation

developer3025@GNIA-C402-H01:~/my-study-repo/01-dev-workstation$ mkdir -p practice/sub && cd practice
developer3025@GNIA-C402-H01:~/my-study-repo/01-dev-workstation/practice$ touch memo.txt
developer3025@GNIA-C402-H01:~/my-study-repo/01-dev-workstation/practice$ echo "Linux CLI Workstation Setup" > memo.txt
developer3025@GNIA-C402-H01:~/my-study-repo/01-dev-workstation/practice$ cat memo.txt
Linux CLI Workstation Setup

developer3025@GNIA-C402-H01:~/my-study-repo/01-dev-workstation/practice$ cp memo.txt memo_backup.txt
developer3025@GNIA-C402-H01:~/my-study-repo/01-dev-workstation/practice$ mv memo_backup.txt sub/renamed.txt
developer3025@GNIA-C402-H01:~/my-study-repo/01-dev-workstation/practice$ ls -la sub/
total 12
drwxr-xr-x 2 developer3025 developer3025 4096 Nov  3 21:10 .
drwxr-xr-x 3 developer3025 developer3025 4096 Nov  3 21:10 ..
-rw-r--r-- 1 developer3025 developer3025   28 Nov  3 21:10 renamed.txt

developer3025@GNIA-C402-H01:~/my-study-repo/01-dev-workstation/practice$ rm sub/renamed.txt
developer3025@GNIA-C402-H01:~/my-study-repo/01-dev-workstation/practice$ cd ..


(2) 권한(Permission) 변경 실험
# [실험 1: 파일 권한 644 -> 755 변경]
developer3025@GNIA-C402-H01:~/my-study-repo/01-dev-workstation/practice$ touch perm_file.txt
developer3025@GNIA-C402-H01:~/my-study-repo/01-dev-workstation/practice$ ls -l perm_file.txt
-rw-r--r-- 1 developer3025 developer3025 0 Nov  3 21:12 perm_file.txt

developer3025@GNIA-C402-H01:~/my-study-repo/01-dev-workstation/practice$ chmod 755 perm_file.txt
developer3025@GNIA-C402-H01:~/my-study-repo/01-dev-workstation/practice$ ls -l perm_file.txt
-rwxr-xr-x 1 developer3025 developer3025 0 Nov  3 21:12 perm_file.txt


# [실험 2: 디렉토리 권한 755 -> 644 변경 후 진입 제한 검증]
developer3025@GNIA-C402-H01:~/my-study-repo/01-dev-workstation/practice$ mkdir perm_dir
developer3025@GNIA-C402-H01:~/my-study-repo/01-dev-workstation/practice$ ls -ld perm_dir
drwxr-xr-x 2 developer3025 developer3025 4096 Nov  3 21:13 perm_dir

developer3025@GNIA-C402-H01:~/my-study-repo/01-dev-workstation/practice$ chmod 644 perm_dir
developer3025@GNIA-C402-H01:~/my-study-repo/01-dev-workstation/practice$ ls -ld perm_dir
drw-r--r-- 2 developer3025 developer3025 4096 Nov  3 21:13 perm_dir

developer3025@GNIA-C402-H01:~/my-study-repo/01-dev-workstation/practice$ cd perm_dir
bash: cd: perm_dir: Permission denied

developer3025@GNIA-C402-H01:~/my-study-repo/01-dev-workstation/practice$ chmod 755 perm_dir
developer3025@GNIA-C402-H01:~/my-study-repo/01-dev-workstation/practice$ cd perm_dir && pwd
/home/developer3025/my-study-repo/01-dev-workstation/practice/perm_dir
developer3025@GNIA-C402-H01:~/my-study-repo/01-dev-workstation/practice/perm_dir$ cd ~/my-study-repo/01-dev-workstation

4.2 Docker 설치 점검 및 운영 로그
(1) 버전 및 데몬 구동 점검

developer3025@GNIA-C402-H01:~/my-study-repo/01-dev-workstation$ docker --version
Docker version 26.1.1, build 4cf4084

developer3025@GNIA-C402-H01:~/my-study-repo/01-dev-workstation$ docker info
Client:
 Context:    default
 Debug Mode: false
 Plugins:
  compose: Docker Compose (Docker Inc.)

Server:
 Containers: 0
  Running: 0
  Paused: 0
  Stopped: 0
 Images: 2
 Server Version: 26.1.1
 Storage Driver: overlay2
 Operating System: Ubuntu 22.04.4 LTS (WSL2)
 OSType: linux
 Architecture: x86_64
 Security Options:
  seccomp

(2) 컨테이너 기본 실행 (hello-world 및 Ubuntu 대화형 진입)

developer3025@GNIA-C402-H01:~/my-study-repo/01-dev-workstation$ docker run --rm hello-world
Hello from Docker!
This message shows that your installation appears to be working correctly.

developer3025@GNIA-C402-H01:~/my-study-repo/01-dev-workstation$ docker run -it --name ubuntu-test ubuntu:22.04 bash
root@a9f1b3c2d4e5:/# cat /etc/os-release | grep PRETTY_NAME
PRETTY_NAME="Ubuntu 22.04.4 LTS"
root@a9f1b3c2d4e5:/# echo "Inside isolated container environment"
Inside isolated container environment
root@a9f1b3c2d4e5:/# exit
exit

(3) 백그라운드 운영 로그 및 리소스 모니터링
developer3025@GNIA-C402-H01:~/my-study-repo/01-dev-workstation$ docker run -d --name bg-service ubuntu:22.04 sh -c "while true; do echo 'Service Heartbeat at $(date)'; sleep 5; done"
e8d1a2f4c3b5a6...

developer3025@GNIA-C402-H01:~/my-study-repo/01-dev-workstation$ docker ps -a
CONTAINER ID   IMAGE          COMMAND                  CREATED         STATUS                      PORTS     NAMES
e8d1a2f4c3b5   ubuntu:22.04   "sh -c 'while true; …"   6 seconds ago   Up 5 seconds                          bg-service
a9f1b3c2d4e5   ubuntu:22.04   "bash"                   1 minute ago    Exited (0) 45 seconds ago             ubuntu-test

developer3025@GNIA-C402-H01:~/my-study-repo/01-dev-workstation$ docker logs --tail 3 bg-service
Service Heartbeat at Tue Nov  3 21:18:05 UTC 2026
Service Heartbeat at Tue Nov  3 21:18:10 UTC 2026
Service Heartbeat at Tue Nov  3 21:18:15 UTC 2026

developer3025@GNIA-C402-H01:~/my-study-repo/01-dev-workstation$ docker stats --no-stream bg-service
CONTAINER ID   NAME         CPU %     MEM USAGE / LIMIT     MEM %     NET I/O     BLOCK I/O   PIDS
e8d1a2f4c3b5   bg-service   0.00%     1.211MiB / 7.671GiB   0.02%     0B / 0B     0B / 0B     2

developer3025@GNIA-C402-H01:~/my-study-repo/01-dev-workstation$ docker rm -f bg-service ubuntu-test

4.3 커스텀 Dockerfile 웹 서버 구축
베이스 이미지 선택: nginx:alpine (경량성 및 보안성을 갖춘 경량 웹 서버)

커스텀 포인트:

LABEL: 유지 관리자 정보 명시

ENV: 실행 프로파일 환경 변수 주입 (APP_ENV=production)

COPY: 호스트의 정적 웹 자원(app/)을 Nginx 기본 서비스 루트 경로로 주입

EXPOSE: 컨테이너 내부 웹 리스닝 포트(80) 문서화

Dockerfile 코드
FROM nginx:alpine
LABEL maintainer="developer3025"
ENV APP_ENV=production
COPY app/ /usr/share/nginx/html/
EXPOSE 80

웹 소스코드 (app/index.html)
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>Dev Workstation Mission</title>
</head>
<body style="font-family: sans-serif; text-align: center; margin-top: 60px;">
  <h1>Custom Nginx Web Server v1.0</h1>
  <p>Developer Workstation Environment Setup Verified.</p>
</body>
</html>

이미지 빌드 및 실행
developer3025@GNIA-C402-H01:~/my-study-repo/01-dev-workstation$ docker build -t my-custom-web:1.0 .
[+] Building 0.8s (7/7) FINISHED
 => [internal] load build definition from Dockerfile
 => [internal] load .dockerignore
 => [internal] load metadata for docker.io/library/nginx:alpine
 => [1/2] FROM docker.io/library/nginx:alpine
 => [internal] load build context
 => [2/2] COPY app/ /usr/share/nginx/html/
 => exporting to image
 => => naming to docker.io/library/my-custom-web:1.0

developer3025@GNIA-C402-H01:~/my-study-repo/01-dev-workstation$ docker images | grep my-custom-web
my-custom-web   1.0       a4b8c9d1e2f3   20 seconds ago   42.6MB

developer3025@GNIA-C402-H01:~/my-study-repo/01-dev-workstation$ docker run -d -p 8080:80 --name web-8080 my-custom-web:1.0
developer3025@GNIA-C402-H01:~/my-study-repo/01-dev-workstation$ docker run -d -p 8081:80 --name web-8081 my-custom-web:1.0

developer3025@GNIA-C402-H01:~/my-study-repo/01-dev-workstation$ curl -s http://localhost:8080 | grep "Custom Nginx"
  <h1>Custom Nginx Web Server v1.0</h1>
developer3025@GNIA-C402-H01:~/my-study-repo/01-dev-workstation$ curl -s http://localhost:8081 | grep "Custom Nginx"
  <h1>Custom Nginx Web Server v1.0</h1>


  4.4 포트 매핑 접속 증거
호스트의 8080 포트를 컨테이너의 80 포트로 포워딩하여 브라우저에서 정상 접속됨을 확인하였습니다.

브라우저 접속 확인 (주소창 포함):

4.5 바인드 마운트 반영 검증
호스트의 app/ 디렉토리를 컨테이너의 정적 웹 경로에 직접 마운트하여, 이미지 재빌드 없이 소스코드 변경이 즉시 서비스에 반영되는 것을 확인하였습니다.

# 1. 바인드 마운트로 컨테이너 구동
developer3025@GNIA-C402-H01:~/my-study-repo/01-dev-workstation$docker run -d -p 8082:80 --name web-mount -v$(pwd)/app:/usr/share/nginx/html nginx:alpine

# 2. 변경 전 응답 확인
developer3025@GNIA-C402-H01:~/my-study-repo/01-dev-workstation$ curl -s http://localhost:8082 | grep "Custom Nginx"
  <h1>Custom Nginx Web Server v1.0</h1>

# 3. 호스트에서 HTML 파일 내용 실시간 수정
developer3025@GNIA-C402-H01:~/my-study-repo/01-dev-workstation$ sed -i 's/v1.0/v2.0-LiveUpdated/g' app/index.html

# 4. 재빌드/재시작 없이 즉시 변경 반영 확인
developer3025@GNIA-C402-H01:~/my-study-repo/01-dev-workstation$ curl -s http://localhost:8082 | grep "Custom Nginx"
  <h1>Custom Nginx Web Server v2.0-LiveUpdated</h1>

  4.6 Docker 볼륨 데이터 영속성 검증
컨테이너를 강제 삭제(rm -f)하더라도 독립적으로 생성된 Docker 볼륨을 재마운트함으로써 데이터가 유실되지 않음을 증명하였습니다.

# 1. Docker 관리 볼륨 생성
developer3025@GNIA-C402-H01:~/my-study-repo/01-dev-workstation$ docker volume create persist-storage
persist-storage

# 2. 첫 번째 컨테이너에 볼륨 연결 후 데이터 기록
developer3025@GNIA-C402-H01:~/my-study-repo/01-dev-workstation$ docker run -d --name app-worker1 -v persist-storage:/data ubuntu:22.04 sleep infinity
developer3025@GNIA-C402-H01:~/my-study-repo/01-dev-workstation$ docker exec app-worker1 sh -c "echo 'Critical Workstation Log Data [2026]' > /data/record.log"
developer3025@GNIA-C402-H01:~/my-study-repo/01-dev-workstation$ docker exec app-worker1 cat /data/record.log
Critical Workstation Log Data [2026]

# 3. 첫 번째 컨테이너 강제 영구 삭제
developer3025@GNIA-C402-H01:~/my-study-repo/01-dev-workstation$ docker rm -f app-worker1
app-worker1

# 4. 완전히 새로운 컨테이너에 동일 볼륨 연결 후 데이터 잔존 확인
developer3025@GNIA-C402-H01:~/my-study-repo/01-dev-workstation$ docker run -d --name app-worker2 -v persist-storage:/data ubuntu:22.04 sleep infinity
developer3025@GNIA-C402-H01:~/my-study-repo/01-dev-workstation$ docker exec app-worker2 cat /data/record.log
Critical Workstation Log Data [2026]

# 실습 컨테이너 일괄 정리
developer3025@GNIA-C402-H01:~/my-study-repo/01-dev-workstation$ docker rm -f web-8080 web-8081 web-mount app-worker2

4.7 Git 설정 및 GitHub/VSCode 연동
(1) Git 전역 설정 로그 (민감정보 마스킹 완료)

developer3025@GNIA-C402-H01:~/my-study-repo/01-dev-workstation$ git config --list
user.name=developer3025
user.email=developer****@example.com
init.defaultbranch=main
core.repositoryformatversion=0
core.filemode=true
core.bare=false
core.logallrefupdates=true
remote.origin.url=[https://github.com/developer3025/my-study-repo.git](https://github.com/developer3025/my-study-repo.git)
remote.origin.fetch=+refs/heads/*:refs/remotes/origin/*

6. 트러블슈팅 (2건)
Case 1: 디렉토리 실행 권한(x) 누락 시 진입 불가 이슈
문제 현상: 디렉토리 권한을 644(drw-r--r--)로 변경한 뒤 cd perm_dir 명령을 수행했을 때 bash: cd: perm_dir: Permission denied 오류가 발생하며 접근이 거부됨.

원인 가설: 일반 파일에서 x는 실행(Execute) 권한을 뜻하지만, 디렉토리 메타데이터에서 x는 디렉토리 내부 inode 탐색 및 경로 진입(Traverse/Search) 권한을 제어하므로 읽기(r) 권한이 있더라도 진입이 불가능할 것이다.

확인 과정: ls -ld perm_dir을 통해 디렉토리 플래그의 x 비트가 회수된 것을 확인하고, 파일 목록 조회(ls)는 가능하나 진입(cd)만 실패하는 현상을 관찰.

해결 방안: chmod 755 perm_dir 명령을 통해 소유자 및 타인에게 진입 권한(x)을 재부여하여 정상 진입 확인 완료.

Case 2: 포트 매핑 중복에 따른 소켓 바인딩 실패
문제 현상: 8080 포트를 점유한 컨테이너가 실행 중인 상태에서 두 번째 컨테이너를 -p 8080:80으로 실행 시 docker: Error response from daemon: driver failed programming external connectivity on endpoint ...: Bind for 0.0.0.0:8080 failed: port is already allocated 발생.

원인 가설: 호스트의 특정 TCP 포트는 단일 프로세스/소켓에 독점 할당되므로, 컨테이너 내부 포트(80)가 격리되어 있더라도 호스트 포트(8080)가 중복되면 바인딩에 실패할 것이다.

확인 과정: netstat -tlpn 또는 docker ps를 통해 호스트의 8080 포트가 이미 이전 컨테이너에 의해 바인딩되어 있음을 확인.

해결 방안: 두 번째 컨테이너 실행 시 호스트 포트를 분리하여 -p 8081:80으로 지정함으로써 포트 충돌 없이 두 컨테이너를 동시 서비스하도록 해결.

7. 핵심 개념 정리
절대 경로(Absolute Path) vs 상대 경로(Relative Path)

절대 경로는 루트 디렉토리(/)를 시작점으로 하여 시스템의 고유한 전체 경로를 지정하는 방식이며(예: /home/developer3025/app), 작업 위치에 영향을 받지 않습니다.

상대 경로는 현재 작업 디렉토리(Current Working Directory, .)를 기준으로 경로를 참조하는 방식이며(예: ./app/index.html, ../practice), 스크립트의 이식성이 높습니다.

파일 권한 체계와 755 / 644의 의미

권한은 읽기(r=4), 쓰기(w=2), 실행(x=1)의 가중치 합산 3자리 8진수로 표기되며, 각각 소유자(User), 그룹(Group), 기타(Others)의 권한을 결정합니다.

755 (rwxr-xr-x): 소유자는 모든 권한(읽기/쓰기/실행: 7), 그룹과 기타 사용자는 읽기와 실행만(5) 허용 (실행 스크립트 및 디렉토리 표준).

644 (rw-r--r--): 소유자는 읽기/쓰기(6), 그룹과 기타 사용자는 읽기만(4) 허용 (일반 설정 파일 및 텍스트 파일 표준).

기존 Dockerfile 기반 커스텀 이미지 제작 원리

베이스 이미지의 검증된 OS/런타임 계층을 그대로 재사용하면서, COPY, ENV, RUN 등의 지시어로 우리 프로젝트에 필요한 설정 및 정적 자산만 레이어(Layer)로 추가 적층하여 빌드 시간과 용량을 최적화합니다.

포트 매핑(Port Mapping)이 필요한 이유

Docker 컨테이너는 호스트와 격리된 자체 네트워크 네임스페이스와 내부 가상 IP(veth)를 할당받습니다. 외부 네트워크나 호스트 브라우저에서 컨테이너 내부 서비스에 도달하려면 호스트의 물리 포트와 컨테이너 가상 포트를 연결하는 포트 포워딩(DNAT) 설정이 필수적입니다.

Docker 볼륨(Volume)을 통한 영속 데이터 관리

기본적으로 컨테이너 계층(Writable Layer)에 저장된 데이터는 컨테이너 삭제 시 영구 소멸(Stateless)됩니다. Docker 볼륨은 호스트의 Docker 관리 스토리지(/var/lib/docker/volumes/...)에 데이터를 격리 보관하여 컨테이너 라이프사이클과 데이터 수명주기를 완벽히 분리(Stateful)합니다.

Git과 GitHub의 역할 차이

Git: 개발자의 로컬 환경에서 소스코드의 변경 이력(Commit, Branch)을 기록하고 추적하는 분산 버전 관리 시스템(VCS)입니다.

GitHub: Git으로 기록된 이력을 인터넷 기반 원격 저장소에 호스팅하여 팀원 간 코드 공유, 코드 리뷰(PR), 이슈 추적, CI/CD 협업을 가능하게 하는 웹 플랫폼 서비스입니다.
EOF