FROM maven:3.9.11-eclipse-temurin-21

WORKDIR /qa-java

COPY pom.xml .
COPY src ./src

CMD ["mvn", "-q", "exec:java", "-Dexec.mainClass=com.pulselab.qa.ValidateApi"]
