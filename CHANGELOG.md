# Changelog

## [0.4.1](https://github.com/unified-systems-com/compliance-core-tap/compare/v0.4.0...v0.4.1) (2026-10-20)


### Features

* **boundary:** default display is the FedRAMP authorization-boundary look ([#50](https://github.com/unified-systems-com/compliance-core-tap/issues/50)) ([2ed3963](https://github.com/unified-systems-com/compliance-core-tap/commit/2ed3963e55728578a7e98c9df02814435683ff2a))
* **compliance_core:** exception fields, exception instance node and edges (PR A) ([17dc3c6](https://github.com/unified-systems-com/compliance-core-tap/commit/17dc3c6a2bb1f44273c78ba398870d58e09b5bf9))
* **compliance_core:** exception fields, exception instance node and edges (PR A) ([721c64a](https://github.com/unified-systems-com/compliance-core-tap/commit/721c64a0fc25e95de58faca92cfbd0e254692a4c))
* **compliance_core:** finding-exception-coverage and exceptions-due-review Search runners (PR B) ([db57d45](https://github.com/unified-systems-com/compliance-core-tap/commit/db57d45dc3cfd913b174db79c887f39183a5810a))
* **compliance_core:** finding-exception-coverage and exceptions-due-review Search runners (PR B) ([a277799](https://github.com/unified-systems-com/compliance-core-tap/commit/a2777990c8307a0da32a84808273055fe1610353))
* EPSS and the rest of CISA's KEV facts on compliance_vulnerability ([e618360](https://github.com/unified-systems-com/compliance-core-tap/commit/e618360541cff6ae0707029cefaaec694e37aac6))
* EPSS and the rest of CISA's KEV facts on compliance_vulnerability [via grype-tap] ([8f7bdb5](https://github.com/unified-systems-com/compliance-core-tap/commit/8f7bdb5bcee83a18eb842f004f745bd560468c4a))
* **finding:** first_detected_at, when the producer first detected a finding ([c7b3dff](https://github.com/unified-systems-com/compliance-core-tap/commit/c7b3dffce23ad1b9805b00992ef45922147b2323))
* **finding:** first_detected_at, when the producer first detected a finding ([ebf3472](https://github.com/unified-systems-com/compliance-core-tap/commit/ebf3472e3a64a3f4c0ac54493bd9ba063d2226ec))
* namespace scanner and scan run keys by producer ([863ec1f](https://github.com/unified-systems-com/compliance-core-tap/commit/863ec1fe9d875352d55dfd487122738982ae4e24))
* **reach:** findings-reached-list rows carry the component they were reached through ([#53](https://github.com/unified-systems-com/compliance-core-tap/issues/53)) ([6672d16](https://github.com/unified-systems-com/compliance-core-tap/commit/6672d16d850da9f787f3d4842850d97e22b76558))
* scan run records its database build; SCANNED_COMPLIANCE_TARGET edge [via grype-tap] ([36bad70](https://github.com/unified-systems-com/compliance-core-tap/commit/36bad70960e49a534706908564bef13483a401a3))
* scan run records its database build; SCANNED_COMPLIANCE_TARGET says what a run examined ([2ae3c86](https://github.com/unified-systems-com/compliance-core-tap/commit/2ae3c860e6a143cff540a2481837b20e8dbd3319))
* **searches:** dimension-coverage, entities per dimension value broken down by entity type ([cebf040](https://github.com/unified-systems-com/compliance-core-tap/commit/cebf040ee3789ae000fa715b5a065a61d169be77))
* **searches:** dimension-coverage, entities per dimension value by entity type ([2144d15](https://github.com/unified-systems-com/compliance-core-tap/commit/2144d15ab6d6a268420d0de07e25cc3f1e61b6e4))
* **searches:** findings-reached-count and findings-reached-list module runners (open findings reached along edge paths, summed without double counting) ([#48](https://github.com/unified-systems-com/compliance-core-tap/issues/48)) ([2a82e35](https://github.com/unified-systems-com/compliance-core-tap/commit/2a82e35a46731d0fd2f6e41c7cec12b750130bfd))
* **searches:** vulnerability-components and component-severity module runners ([#44](https://github.com/unified-systems-com/compliance-core-tap/issues/44)) ([5b7dd12](https://github.com/unified-systems-com/compliance-core-tap/commit/5b7dd123701465d4002e57cd84f083780156b55e))
* **searches:** vulnerability-components rows carry component_items, structured links per component ([#46](https://github.com/unified-systems-com/compliance-core-tap/issues/46)) ([df4ab4d](https://github.com/unified-systems-com/compliance-core-tap/commit/df4ab4ddd5d05ffb817db7622e416e58a1c37e13))
* vulnerability, scanner and scan_run types, with the scan edges ([fed4a70](https://github.com/unified-systems-com/compliance-core-tap/commit/fed4a70faaa241a1bbf9235fe4bbe51022b9f9f5))
* vulnerability, scanner and scan_run types, with the scan edges [via rampart-pg] ([1a0a2b8](https://github.com/unified-systems-com/compliance-core-tap/commit/1a0a2b855b3e2cd1c57645d06371c3210c65de37))


### Bug Fixes

* **boot:** pin the commit beside every git source's rev in the CI record ([183212e](https://github.com/unified-systems-com/compliance-core-tap/commit/183212ecb5c996d9b7908559dbf9c60abab14cba))
* **boot:** pin the commit beside every git source's rev in the CI record [via bom-bom] ([9d469fd](https://github.com/unified-systems-com/compliance-core-tap/commit/9d469fdf7a95e39f24860728f638014726b8ea0a))
* **compliance_core:** build the test cases in a loop, not as a bare tuple expression ([123d060](https://github.com/unified-systems-com/compliance-core-tap/commit/123d0606dd2a60a0747d88610f988f79aaf66046))
* **compliance_core:** coverage needs at least one anchor whatever anchor_count says; drop assert ([ac5c086](https://github.com/unified-systems-com/compliance-core-tap/commit/ac5c086469974ad3c33f93d2553452046356cb1a))
* **compliance_core:** share field schemas between CRUD and validation; test justification on replace ([9dcb5db](https://github.com/unified-systems-com/compliance-core-tap/commit/9dcb5db3a95611cb4b7229ed5ae49ca73a166bfa))
* **finding:** refuse a bare date for first_detected_at; prove history keeps a replaced value ([7a0c697](https://github.com/unified-systems-com/compliance-core-tap/commit/7a0c6970809f667434a32696ce53a43a5da884eb))
* say cardinality is the producer's, drop the SVG comments ([15e5751](https://github.com/unified-systems-com/compliance-core-tap/commit/15e5751958ec5de50af02c6e7fb399f0e99da0f3))
* **schema:** declare format date-time and date on the timestamp and date fields ([#41](https://github.com/unified-systems-com/compliance-core-tap/issues/41)) ([d084e63](https://github.com/unified-systems-com/compliance-core-tap/commit/d084e638b7636e4ca76752e498c0aa674205233b))


### Documentation

* **spec:** say the KEV-detail pairing is the writer's duty, not enforced ([06be738](https://github.com/unified-systems-com/compliance-core-tap/commit/06be7383f79ad9e1ba198b32bba29cb8e6b5c54f))
