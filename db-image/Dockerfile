FROM postgres:17

# dump.sql을 컨테이너가 첫 기동 시 자동 실행되는 디렉터리에 복사
COPY dump.sql /docker-entrypoint-initdb.d/
