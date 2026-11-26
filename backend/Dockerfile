# Build Stage using Maven with OpenJDK 21
FROM maven:3.9.8-eclipse-temurin-21-alpine AS builder
WORKDIR /app
COPY pom.xml .
RUN mvn dependency:go-offline -B
COPY src ./src
RUN mvn clean package -DskipTests

# Production Stage with JDK 21 (for javac) + Python 3 (for live judge execution)
FROM eclipse-temurin:21-jdk-alpine
WORKDIR /app
RUN apk add --no-cache python3 \
    && addgroup -S appgroup && adduser -S appuser -G appgroup
USER appuser
COPY --from=builder /app/target/*.jar app.jar
EXPOSE 8080
ENTRYPOINT ["java", "-jar", "app.jar"]
