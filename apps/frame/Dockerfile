FROM node:22-alpine AS build

RUN apk add --no-cache git

WORKDIR /src

# Changes whenever the fork's main moves, so a redeploy picks up new dashboard commits.
ADD https://api.github.com/repos/SathyaBhat/photo-frame-dashboard/git/refs/heads/main /tmp/main.json
RUN git clone --depth 1 https://github.com/SathyaBhat/photo-frame-dashboard.git .

WORKDIR /src/dashboard
RUN npm ci && npx vite build --base /frame/

FROM nginx:alpine

COPY --from=build /src/dashboard/dist /usr/share/nginx/html
