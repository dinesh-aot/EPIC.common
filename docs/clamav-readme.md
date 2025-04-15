# Accessing ClamAV service from silver

Full installation of ClamAv demands a lot of resources.so the approach is to access the clamav in silver cluster and set up the connectivity using TSC
---

## Step 1: Apply the TSC to the Namespace

Create your tsc  file [tsc_clamav_service.yaml](../deployments/tsc_clamav_service.yaml)
```bash
oc apply -f tsc.yaml -n namespace
```

---

## Step 2: Check the TSC and TransportServer

List your TransportServerClaims to verify it's working:

```bash
oc get tscs -n namespace
```

Then, get the assigned host and port from the generated TransportServer:

```bash
oc get ts -n namespace
```

Look for:

- Virtual Server Address (e.g., `142.34.194.68`)
- Virtual Server Port (e.g., `16504`)

---

## Step 3: Test Connectivity from Inside a Pod

Run this from any OpenShift pod (e.g., debug pod):

```bash
timeout 5 bash -c ">/dev/tcp/<VIRTUALSERVERADDRESS>/<VIRTUALSERVERPORT>"; echo $?
```

Return Codes:
- 0: Connected
- 1: Connection refused
- 124: Timed out

---

If the connection is successful (0 return code), the service is exposed .

## Additional notes:

### Step 4: Test for Virus Positive Case (EICAR)

To simulate a virus detection, create an EICAR test file inside your pod:

```bash
echo "X5O!P%@AP[4\\PZX54(P^)7CC)7}\$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!\$H+H*" > /tmp/eicar.com
```

Run the virus scanner job from your Python container:

```bash
python3 invoke_jobs.py SCAN_VIRUS /tmp/eicar.com
```

This should trigger a "virus detected" response if ClamAV is correctly connected.

---

### Cleanup

To delete your TransportServerClaim:

```bash
oc delete tsc clamav-tsc -n 6cdc9e-prod
```

---

## Notes

- The Python service uses `clamd` to stream and scan files using ClamAV.
- S3 files can also be scanned by passing an `s3://bucket/key` path to the same job.
- See your `invoke_jobs.py` and `VirusScanner` class for implementation details.